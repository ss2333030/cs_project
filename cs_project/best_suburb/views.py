"""
This file defines the controller part of the MVC architecture.

This module defines a set of HTTP request handlers for handling
HTTP requests made by the user. Each request handler handles requests
sent by the user to a certain path. It processes the request and then 
sends back the response to the user.
"""

__author__ = "Feng Ji & Ngok Yu"

from ast import Sub
from logging.handlers import QueueListener

from django.http import HttpResponse
import imp
from json.encoder import INFINITY
from googlemaps import Client
from django.db.models import Max, Min
from multiprocessing.sharedctypes import Value
from os import lstat
from re import T
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar, Line, Gauge, Liquid
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
from pyecharts.faker import Faker
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
import requests
import math
from .models import Suburb, University
from typing import Dict, List, Type, TypeVar, Callable
import requests
import json

T = TypeVar("T")
U = TypeVar("U")

# First - level separator |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
# Second - level separator ################################################################################################
# Third - level separator =================================================================================================


# ||||||||||||||||||||||||||| Helper functions and structures |||||||||||||||||||||||||||||||||

# ####################### Declare the API key and a new instance of goole map ################
API_KEY = "AIzaSyDRsqK_7w_eBkmNJZUczRnyC9jJx5gj5xQ"

INFINITY = 10000000  # A constant that represents infinity in this app
UNDEFINED = -1  # A constant that represents undefined in this app


def filter(lst: List[T], f: Callable[[T], bool]) -> List[T]:
    """ A generic function for filtering elements in the input list.

    :input lst: a list of elements of type T. For example, T can be int, or str, or bool, or user-defined object, etc.
    :input f: a function that takes as input an element of the list and then returns either True or False. It is a condition.
    :output: the elements in the input list that meet the given condition
    """

    return lst if len(lst) == 0 else ([lst[0]] + filter(lst[1:], f) if f(lst[0]) else filter(lst[1:], f))


def map(lst: List[T], f: Callable[[T], U]) -> List[U]:
    """ A generic function for mapping elements in the input list.

    :input lst: a list of elements of type T. For example, T can be int, or str, or bool, or user-defined object, etc.
    :input f: a function that takes as input an element of type T of the list and then maps it to a new value of type U. It is a mapper function.
    :output: a list of elements of type U. Its length is the same as that of the input list.
    """

    return lst if len(lst) == 0 else [f(lst[0])] + map(lst[1:], f)


class Location:
    """ A class that represents a geographical location. """

    def __init__(self, latitude: float, longitude: float) -> None:
        self.__latitude: float = latitude  # The latitude of the location
        self.__longitude: float = longitude  # The longitude of the location

    def get_latitiude(self) -> float:
        return self.__latitude

    def get_longitude(self) -> float:
        return self.__longitude


def haversine_distance(l1: Location, l2: Location) -> float:
    """ Compute the distance between two locations using coordinates. 
        This code was taken from https://cloud.google.com/blog/products/maps-platform/how-calculate-distances-map-maps-javascript-api.

    :input l1: a location
    :input l2: another location
    :output: the distance between the two locaitons in kilometer
    """

    R = 6371.0710
    # Radius of the Earth in miles
    rlat1 = l1.get_latitiude() * (math.pi / 180)
    # Convert degrees to radians
    rlat2 = l2.get_latitiude() * (math.pi / 180)
    # Convert degrees to radians
    difflat = rlat2 - rlat1
    # Radian difference (latitudes)
    difflon = (l2.get_longitude() - l1.get_longitude()) * (math.pi / 180)
    # Radian difference (longitudes)

    d = (
        2
        * R
        * math.asin(
            math.sqrt(
                math.sin(difflat / 2) * math.sin(difflat / 2)
                + math.cos(rlat1)
                * math.cos(rlat2)
                * math.sin(difflon / 2)
                * math.sin(difflon / 2)
            )
        )
    )

    return d


def add_photo(s: dict) -> dict:
    """ Add one photo to the given suburb. In this way, 
        we can see a photo of the suburb on the list page.
    """

    # Check if preconditions are met
    try:
        temp = s["name"]
        temp = s["latitude"]
        temp = s["longitude"]
    except KeyError:
        raise AssertionError("The given suburb is invalid.")

    assert s["name"] != "", "The given suburb has an invalid name."
    assert 0 <= s["latitude"] <= 90 or - \
        90 <= s["latitude"] <= 0, "The given suburb has an invalid latitude."
    assert 0 <= s["longitude"] <= 180 or - \
        180 <= s["longitude"] <= 0, "The given suburb has an invalid longitude."

    # This builds the URL required by Google Maps Platform - Places API - Place Search - Find Place
    URL = (
        "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
        + s["name"]
        + "&inputtype=textquery&locationbias=circle%3A2000%40"
        + str(s["latitude"])
        + "%2C"
        + str(s["longitude"])
        + "&fields=place_id%2Cphotos&key="
        + API_KEY
    )

    # Send a GET request to Google Maps Platform - Places API - Place Search - Find Place
    response = requests.request("GET", URL).json()

    assert response["status"] != "INVALID_REQUEST" and response["status"] != "REQUEST_DENIED"

    if len(response["candidates"]) < 1:  # If the API didn't find the given suburb at all
        s["place_id"] = ""  # This represents that this suburb doesn't have a place id
        # Use the default photo instead
        s["photo"] = "/static/best_suburb/images/suburb.png"
    else:
        try:
            response["candidates"][0]["photos"]
        except KeyError:
            # If the API didn't return any photos
            s["place_id"] = response["candidates"][0]["place_id"]
            # Use the default photo instead
            s["photo"] = "/static/best_suburb/images/suburb.png"
        else:
            photo_reference = response["candidates"][0]["photos"][0]["photo_reference"]
            # Build the URL for the photo
            photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
            s["place_id"] = response["candidates"][0]["place_id"]
            s["photo"] = photo

    return s


def get_qualified_suburbs(uni_id: int, rent_min: int, rent_max: int, crime_rate_max: int, distance_min: int, distance_max: int) -> List[dict]:
    """ Return the list of suburbs that meet the conditions specified by the user.

    :input uni_id: the database ID of the university
    :input rent_min: minimum average rent
    :input rent_max: maximum average rent
    :input crime_rate_max: maximum crime rate
    :input distance_min: minimum distance
    :input distance_max: maximum distance
    :output: a list of Suburb objects
    """

    # Find the University object whose id equals to uni_id
    university = University.objects.get(id=uni_id)

    # Get the list of suburbs that meet the specified average rent and crime rate
    suburbs = Suburb.objects.filter(
        average_rent__gte=rent_min, average_rent__lte=rent_max, crime_rate__lte=crime_rate_max).values()

    # Filter the suburbs again by distance
    def condition(e: dict) -> bool:
        # Get the location of the suburb
        l1 = Location(e["latitude"], e["longitude"])
        # Get the location of the university
        l2 = Location(university.latitude, university.longitude)
        # Add distance to the suburb
        e["distance"] = haversine_distance(l1, l2)
        return distance_min <= e["distance"] <= distance_max

    # Get the list of suburbs that meet the specified average rent, distance, and crime rate
    results = filter(suburbs, condition)

    # Add one photo to each suburb
    return map(results, add_photo)


def get_distance(suburb: dict, university: dict) -> float:
    """ Calculate the distance between the given suburb and university. 

    :input suburb: the target suburb
    :input university: the user's university
    :output: the distance between the suburb and the university
    """

    l1 = Location(suburb["latitude"], suburb["longitude"])
    l2 = Location(university["latitude"], university["longitude"])
    return round(haversine_distance(l1, l2), 2)


def get_photos(place_id: str):
    """ Get a collection of photos for a given suburb using its place_id.

    :input place_id: the place_id of the suburb
    :output: a list of photos of the suburb    
    """

    # Build the URL and send an HTTP request to Google Maps Platform - Places API - Place Details
    URL = f"https://maps.googleapis.com/maps/api/place/details/json?fields=photos&place_id={place_id}&key={API_KEY}"
    response = requests.request("GET", URL).json()

    photos = []

    try:
        for i in range(len(response["result"]["photos"])):
            # Build the URL for this photo
            photo_reference = response["result"]["photos"][i]["photo_reference"]
            photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"

            # Add this photo to the photo list
            photos.append(photo)
    except KeyError:  # If no photos were returned for the given suburb
        photos.append("/static/best_suburb/images/suburb.png")

    return photos


def convert_coordinates(s: dict) -> None:
    """ Convert the geographic coordinates of the given suburb to the format ready for display.

    :input s: the given suburb
    """

    # Get the latitude and longitude of the given suburb
    latitude = s["latitude"]
    longitude = s["longitude"]

    # Convert the latitude and longitude of the given suburb to the format ready for display
    if latitude >= 0 and longitude >= 0:
        s["latitude"] = abs(latitude)
        s["hemisphere_latitude"] = "N"
        s["longitude"] = abs(longitude)
        s["hemisphere_longitude"] = "E"
    elif latitude >= 0:
        s["latitude"] = abs(latitude)
        s["hemisphere_latitude"] = "N"
        s["longitude"] = abs(longitude)
        s["hemisphere_longitude"] = "W"
    elif longitude >= 0:
        s["latitude"] = abs(latitude)
        s["hemisphere_latitude"] = "S"
        s["longitude"] = abs(longitude)
        s["hemisphere_longitude"] = "E"
    else:
        s["latitude"] = abs(latitude)
        s["hemisphere_latitude"] = "S"
        s["longitude"] = abs(longitude)
        s["hemisphere_longitude"] = "W"


def validate_input(uni_id: str, distance_min: str, distance_max: str, crime_rate_max: str, rent_min: str, rent_max: str) -> dict:
    """ Convert input values into appropriate format and validate input values."""

    # Convert input values into appropriate data type
    uni_id = int(uni_id)
    distance_min = int(distance_min)
    distance_max = int(distance_max)
    crime_rate_max = int(crime_rate_max)
    rent_min = int(rent_min)
    rent_max = int(rent_max)

    # Validate the provided university ID
    university = University.objects.get(id=uni_id)
    if university is None:
        raise ValueError("The provided university ID is incorrect!")

    # Validate the provided minimum distance
    if (distance_min < 1 and distance_min != UNDEFINED) or distance_min > 20:
        raise ValueError("The provided minimum distance is incorrect!")

    # Validate the provided maximum distance
    if (distance_max < 1 and distance_max != UNDEFINED) or distance_max > 20:
        raise ValueError("The provided maximum distance is incorrect!")

    # Validate the provided maximum crime rate
    if (crime_rate_max < 1000 and crime_rate_max != UNDEFINED) or crime_rate_max > 30000:
        raise ValueError("The provided maximum crime rate is incorrect!")

    # Validate the provided minimum average rent
    if (rent_min < 100 and rent_min != UNDEFINED) or rent_min > 700:
        raise ValueError("The provided minimum average rent is incorrect!")

    # Validate the provided maximum average rent
    if (rent_max < 100 and rent_max != UNDEFINED) or rent_max > 700:
        raise ValueError("The provided maximum average rent is incorrect!")

    # Define some conversion functions
    def convert_min(x): return 0 if x < 0 else x
    def convert_max(x): return INFINITY if x < 0 else x

    return {
        "uni_id": uni_id,
        "distance_min": convert_min(distance_min),
        "distance_max": convert_max(distance_max),
        "crime_rate_max": convert_max(crime_rate_max),
        "rent_min": convert_min(rent_min),
        "rent_max": convert_max(rent_max)
    }

# ||||||||||||||||||||||||||||||||||| Request handlers |||||||||||||||||||||||||||||||||||||||||||||||||||


def direction(request):
    """ Request handler for getting information about public transport.

    :input request.GET.get("suburb_place_id"): the place id of the suburb
    :input request.GET.get("desired_place_place_id"): the place id of the place entered by the user
    :output: the route from the suburb to the place
    """

    # Get the place id of the current suburb and the entered location
    suburb_place_id = request.GET.get("suburb_place_id")
    desired_place_place_id = request.GET.get("desired_place_place_id")

    if suburb_place_id == "":
        return HttpResponse(status=404)

    # Build the URL and send an HTTP request to Google Maps Platform - Directions API
    URL = f"https://maps.googleapis.com/maps/api/directions/json?destination=place_id:{desired_place_place_id}&origin=place_id:{suburb_place_id}&mode=transit&key={API_KEY}"
    response = requests.request("GET", URL).json()

    if len(response["routes"]) < 1:
        return HttpResponse(status=404)
    else:
        # Get details
        try:
            end_address = response["routes"][0]["legs"][0]["end_address"]
            distance = response["routes"][0]["legs"][0]["distance"]
            duration = response["routes"][0]["legs"][0]["duration"]
        except KeyError:
            return HttpResponse(status=404)

        return JsonResponse({"end_address": end_address, "distance": distance, "duration": duration})
    # details = []

    # for i in range(len(response["routes"][0]["legs"][0]["steps"])):
    #     if response["routes"][0]["legs"][0]["steps"]["travel_mode"] == "TRANSIT":
    #         details.append(
    #             {
    #                 "duration": response["routes"][0]["legs"][0]["steps"]["duration"],
    #                 "departure_stop": response["routes"][0]["legs"][0]["steps"]["transit_details"][
    #                     "departure_stop"
    #                 ]["name"],
    #                 "arrival_stop": response["routes"][0]["legs"][0]["steps"]["transit_details"][
    #                     "arrival_stop"
    #                 ]["name"],
    #                 "type": response["routes"][0]["legs"][0]["steps"]["transit_details"]["lines"][
    #                     "vehicle"
    #                 ]["name"],
    #                 "transit_line_name": response["routes"][0]["legs"][0]["steps"][
    #                     "transit_details"
    #                 ]["lines"]["name"],
    #                 "headsign": response["routes"][0]["legs"][0]["steps"]["transit_details"][
    #                     "headsign"
    #                 ],
    #             }
    #         )
    #     else:
    #         details.append(
    #             {
    #                 "duration": response["routes"][0]["legs"][0]["steps"]["duration"],
    #                 "distance": response["routes"][0]["legs"][0]["steps"]["duration"],
    #             }
    #         )


def places(request):
    """ Request handler for getting a list of candidate places based on the user input.
        This is used to achieve autocompletion on the info page.

    :input request.GET.get("place"): the place entered by the user
    :output: A list of candidate places
    """

    # Build the URL and send an HTTP request to Google Maps Platform - Places API - Place Autocomplete
    URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + \
        request.GET.get("place") + \
        f"&ipbias&components=country:au&key={API_KEY}"
    response = requests.request("GET", URL).json()

    return JsonResponse(response)


def index(request):
    """ Request handler for the path "/". It sends back the home page to the user.
    This function will be called whenever the user makes a request to the path "/".
    """

    # Send back the page "index.html"
    return render(request, "best_suburb/index.html", {"universities": University.objects.all().values()})


def suburbs(request):
    """ Request handler for the path "/suburbs". It first processes the request
        and then sends back a list of suburbs that meet the conditions specified by
        the user. This function will be called whenever the user makes a request to the path "/suburbs".

    :input request: an object/dictionary that represents an HTTP request. The most important 
                    property/field it has is a field called "GET", which contains input parameters in a GET request.
                    request.GET is also an object/dictionary that has six fields: the database ID of the user's university,
                    the minimum distance from the university (in kilometer), the maximum distance from the university (in kilometer),
                    the maximum crime rate in a suburb (per 100,000), the minimum average rent in a suburb (in australian dollar),
                    the maximum average rent in a suburb (also in australian dollar).
    :output: a list of suburbs that meet the given conditions.
    """

    # Check if the input values are valid or not and convert the input values into appropriate format
    try:
        parameters = validate_input(
            request.GET.get("uni_id"),
            request.GET.get("distance_min"),
            request.GET.get("distance_max"),
            request.GET.get("crime_rate_max"),
            request.GET.get("rent_min"),
            request.GET.get("rent_max"),
        )
    except ValueError or TypeError:  # Incorrect input
        return HttpResponse(status=404)
    except Exception:  # Something went wrong
        return HttpResponse(status=400)

    # Get the list of suburbs that meet given conditions
    qualified_suburbs = get_qualified_suburbs(
        parameters["uni_id"],
        parameters["rent_min"],
        parameters["rent_max"],
        parameters["crime_rate_max"],
        parameters["distance_min"],
        parameters["distance_max"]
    )

    # Convert the list of suburbs into a python list
    data = []
    for i in range(len(qualified_suburbs)):
        data.append(qualified_suburbs[i])

    # Return the list of suburbs in JSON format
    return JsonResponse(data, safe=False)


def list(request):
    """ Request handler for the path "/list". 
        It sends back a template (the list page) to the user. 
        This function will be called whenever the user makes a request to the path "/list".

    :input request: an object/dictionary that represents an HTTP request. However, it is not used
                    in this function.
    :output: a response that contains the list page.
    """

    return render(request, "best_suburb/list.html", {
        "universities": University.objects.all().values()
    })


def info(request):
    """ Request handler for the path "/info".
            It sends back a template (the info page) to the user.
            This function will be called whenever the user makes a request to the path "/info".

        :input request: an object/dictionary that represents an HTTP request. However, it is not used
                        in this function.
        :output: a response that contains the info page.
        """

    # Find the requested suburb using its id
    suburb = Suburb.objects.filter(
        id=int(request.GET.get("suburb_id"))).values()[0]

    # Find the user's university using its id
    university = University.objects.filter(
        id=int(request.GET.get("uni_id"))).values()[0]

    # Add additional attributes to the suburb
    suburb["photos"] = get_photos(request.GET.get("place_id"))
    suburb["distance"] = get_distance(suburb, university)
    suburb["place_id"] = request.GET.get("place_id")
    convert_coordinates(suburb)

    # get the char
    myechar = get_crimerate_char(suburb)
    recome = recom_char()
    average_char = get_average_char(suburb)

    return render(
        request,
        "best_suburb/info.html",
        {
            "suburb": suburb,
            "uni_name": university["name"],
            "crime_char": myechar.render_embed(),
            "recom_char": recome,
            "average_char": average_char.render_embed(),
        },
    )


def get_crimerate_char(suber_name):
    """ This function is create a line chart using pyechart.
        This chart is about this suburb crime rate in ten year

        :input request:  the suburb name
        :output: the line chart about this suburb crime rate in ten year
        """

    item_color_js_2 = """new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                                            offset: 0,
                                            color: 'rgb(129, 227, 238)'
                                        }, {
                                            offset: 1,
                                            color: 'rgb(25, 183, 207)'
                                        }])"""
    x_data = ["2013", "2014", "2015", "2016",
              "2017", "2018", "2019", "2020", "2021"]
    y_data = [
        suber_name.get("crime_rate_in_2013"),
        suber_name.get("crime_rate_in_2014"),
        suber_name.get("crime_rate_in_2015"),
        suber_name.get("crime_rate_in_2016"),
        suber_name.get("crime_rate_in_2017"),
        suber_name.get("crime_rate_in_2018"),
        suber_name.get("crime_rate_in_2019"),
        suber_name.get("crime_rate_in_2020"),
        suber_name.get("crime_rate_in_2021"),
    ]

    c = (
        Line(init_opts=opts.InitOpts(width="500px", height="300px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            itemstyle_opts=opts.ItemStyleOpts(color=JsCode(item_color_js_2)),
            series_name="crime rate",
            stack="total",
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=suber_name.get("name") + " crime rate in ten year",
                pos_left="center",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(
                is_show=True, pos_left="70%", pos_bottom="80%"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="      Crime rate",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category", name="Years", boundary_gap=False
            ),
        )
    )
    return c


def get_average_char(suber_name):
    """ This function is create a line chart using pyechart.
            This chart is about this suburb average rent  in ten year

            :input request:  the suburb name
            :output: the line chart about this suburb average rent in ten year
            """

    x_data = ["2013", "2014", "2015", "2016",
              "2017", "2018", "2019", "2020", "2021"]
    y_data = [
        suber_name.get("averagerent_in_2013"),
        suber_name.get("averagerent_in_2014"),
        suber_name.get("averagerent_in_2015"),
        suber_name.get("averagerent_in_2016"),
        suber_name.get("averagerent_in_2017"),
        suber_name.get("averagerent_in_2018"),
        suber_name.get("averagerent_in_2019"),
        suber_name.get("averagerent_in_2020"),
        suber_name.get("averagerent_in_2021"),
    ]

    c = (
        Line(init_opts=opts.InitOpts(width="500px", height="300px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="average rent",
            stack="total",
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=suber_name.get("name") + " average rent in ten year",
                pos_left="center",
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(
                is_show=True, pos_left="70%", pos_bottom="80%"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="      Average rent",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}$"),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category", name="Years", boundary_gap=False
            ),
        )
    )
    return c


def recom_char():
    """ This function is create a water chart using pyechart.
               This chart is about this suburb  Recommendation Index  in ten year

               :input request:  the suburb name
               :output: the line chart about this suburb Recommendation Index using our  Recommendation Index system
               """

    liquid = (
        Liquid(init_opts=opts.InitOpts(width="300px", height="300px"))
        .add("", [0.52, 0.44])
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="  Recommendation Index",
                pos_left="center",
                title_textstyle_opts=opts.TextStyleOpts(color="red"),
                pos_bottom="13%",
            ),
        )
    )
    max_crimerate = (Suburb.objects.all().aggregate(Max("crime_rate"))).get(
        "crime_rate__max"
    )
    min_crimerate = (Suburb.objects.all().aggregate(Min("crime_rate"))).get(
        "crime_rate__min"
    )
    max_averagerent = (Suburb.objects.all().aggregate(Max("average_rent"))).get(
        "average_rent__max"
    )
    min_averagerent = (Suburb.objects.all().aggregate(Min("average_rent"))).get(
        "average_rent__min"
    )
    print(max_crimerate)
    print(min_crimerate)
    print(max_averagerent)
    print(min_averagerent)

    return liquid.render_embed()


def recommended_system(qualified_suburbs):

    new_list = []
    max_crimerate = (
        Suburb.objects.all().aggregate(Max("crime_rate")).get("crime_rate__max")
    )
    min_crimerate = (
        Suburb.objects.all().aggregate(Min("crime_rate")).get("crime_rate__min")
    )
    max_averagerent = (
        Suburb.objects.all().aggregate(Max("average_rent")).get("average_rent__max")
    )

    min_averagerent = (
        Suburb.objects.all().aggregate(Min("average_rent")).get("average_rent__min")
    )

    lenth = len(qualified_suburbs)
    for i in range(0, lenth):
        suburb = qualified_suburbs[i]

    return new_list


def get_suburb_score(suburb, max_crime, min_crime, max_rent, min_rent):
    score = 0
    rent = suburb.get("average_rent")
    crime = suburb.get("crime_rate")
    return score
