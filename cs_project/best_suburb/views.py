from ast import Sub
# from asyncio.windows_events import NULL
from http.client import HTTPResponse
import imp

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
from typing import List, Type, TypeVar, Callable
import requests
import json


T = TypeVar("T")
U = TypeVar("U")

################################# Helper functions and structures ###############################
API_KEY = "AIzaSyDRsqK_7w_eBkmNJZUczRnyC9jJx5gj5xQ"


def filter(lst: List[T], f: Callable[[T], bool]):
    return (
        lst
        if len(lst) == 0
        else ([lst[0]] + filter(lst[1:], f) if f(lst[0]) else filter(lst[1:], f))
    )


def map(lst: List[T], f: Callable[[T], U]):
    return lst if len(lst) == 0 else [f(lst[0])] + map(lst[1:], f)


class Location:
    def __init__(self, latitude, longitude):
        self.__latitude = latitude
        self.__longitude = longitude

    def get_latitiude(self):
        return self.__latitude

    def get_longitude(self):
        return self.__longitude


def haversine_distance(l1: Location, l2: Location):
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


def addUni(request):
    University = University(name="MMM", suburbname="Sname", location="33,33")
    University.save()
    return HttpResponse("<p>Success<p>")


def search():
    PrintSuburb = Suburb.objects.all()
    for i in PrintSuburb:
        print(i.name)
    return 0


#     return photos
# def get_photos(suburb: str):
#     suburb = Suburb.objects.filter(id=suburb)[0]
#     URL = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={suburb.name}&inputtype=textquery&locationbias=circle%3A2000%40{suburb.latitude}%2C{suburb.longitude}&fields=formatted_address%2Cname%2Crating%2Cplace_id%2Cphotos&key={API_KEY}"
#     payload = {}
#     headers = {}

#     response = requests.request("GET", URL, headers=headers, data=payload).json()
#     photos = []

#     for i in range(len(response["candidates"]["photos"])):
#         photo_reference = response["candidates"]["photos"][i]["photo_reference"]
#         PHOTO_URL = f"https://maps.googleapis.com/maps/api/place/photo?&photo_reference={photo_reference}&key={API_KEY}"
#         payload_2 = {}
#         headers_2 = {}
#         response = requests.request("GET", PHOTO_URL, headers=headers_2, data=payload_2)
#         photos.append(response.text)

#     return photos


def get_qualified_suburbs(
    uni: str,
    rent_min: int,
    rent_max: int,
    crime_rate_max: int,
    distance_min: int,
    distance_max: int,
):
    """Returns the correct suburbs according to user input."""

    # Get the university
    university = University.objects.filter(id=uni)[0]

    # Get the list of qualified suburbs
    suburbs = Suburb.objects.filter(
        average_rent__gte=rent_min,
        average_rent__lte=rent_max,
        crime_rate__lte=crime_rate_max,
    ).values()

    # Filter suburbs by distance
    def condition(e: Suburb):
        l1 = Location(e["latitude"], e["longitude"])
        l2 = Location(university.latitude, university.longitude)
        return distance_min <= haversine_distance(l1, l2) <= distance_max

    # Add a photo property to the suburbs

    def bind_suburb_to_google_map(e: Suburb) -> Suburb:
        URL = (
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
            + e["name"]
            + "&inputtype=textquery&locationbias=circle%3A2000%40"
            + str(e["latitude"])
            + "%2C"
            + str(e["longitude"])
            + "&fields=formatted_address%2Cname%2Crating%2Cplace_id%2Cphotos&key="
            + API_KEY
        )
        payload = {}
        headers = {}

        response = requests.request("GET", URL, headers=headers, data=payload).json()

        try:
            photo_reference = response["candidates"][0]["photos"][0]["photo_reference"]
            photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"


            e["photo"] = photo_url
            e["place_id"] = response["candidates"][0]["place_id"]

        except:
            e["photo"] = "/static/best_suburb/images/suburb.png"
            e["place_id"] = response["candidates"][0]["place_id"]
        return e

    return map(filter(suburbs, condition), bind_suburb_to_google_map)


def get_distance(suburb: Suburb, uni: str):
    # Get the university
    university = University.objects.filter(id=uni).values()[0]

    l1 = Location(suburb["latitude"], suburb["longitude"])
    l2 = Location(university["latitude"], university["longitude"])
    return round(haversine_distance(l1, l2), 2)


def get_photos(place_id: str):
    """Get a collection of photos for a given place."""
    URL = f"https://maps.googleapis.com/maps/api/place/details/json?fields=formatted_address%2Cname%2Cphotos&place_id={place_id}&key={API_KEY}"
    payload = {}
    headers = {}

    response = requests.request("GET", URL, headers=headers, data=payload).json()

    photos = []
    try:
        for i in range(len(response["result"]["photos"])):
            photo_reference = response["result"]["photos"][i]["photo_reference"]
            photo = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photo_reference={photo_reference}&key={API_KEY}"
            photos.append(photo)
    except:
        photos.append("/static/best_suburb/images/suburb.png")
    return photos


def convert_coordinates(e: Suburb) -> Suburb:
    latitude = e["latitude"]
    longitude = e["longitude"]

    if latitude >= 0 and longitude >= 0:
        e["latitude"] = abs(latitude)
        e["hemisphere_latitude"] = "N"
        e["longitude"] = abs(longitude)
        e["hemisphere_longitude"] = "E"
    elif latitude >= 0:
        e["latitude"] = abs(latitude)
        e["hemisphere_latitude"] = "N"
        e["longitude"] = abs(longitude)
        e["hemisphere_longitude"] = "W"
    elif longitude >= 0:
        e["latitude"] = abs(latitude)
        e["hemisphere_latitude"] = "S"
        e["longitude"] = abs(longitude)
        e["hemisphere_longitude"] = "E"
    else:
        e["latitude"] = abs(latitude)
        e["hemisphere_latitude"] = "S"
        e["longitude"] = abs(longitude)
        e["hemisphere_longitude"] = "W"
    return e


#################################### Views #######################################################
def places(request):
    """Request handler for getting a list of places."""

    URL = (
        "https://maps.googleapis.com/maps/api/place/autocomplete/json?input="
        + request.GET.get("place")
        + "&ipbias&components=country:au&key=AIzaSyDRsqK_7w_eBkmNJZUczRnyC9jJx5gj5xQ"
    )
    payload = {}
    headers = {}
    response = requests.request("GET", URL, headers=headers, data=payload).json()
    return JsonResponse(response)


def index(request):
    """Request handler for the path "/". This function will be
    called whenever the client requests the path "/".
    """

    # This returns the page "index.html"
    return render(
        request, "best_suburb/index.html", {"universities": University.objects.all()}
    )


def suburbs(request):
    """Request handler for the path "/suburbs". This function will
    be called whenever the client requests the path "/suburbs".
    """

    # If this is a POST request, this means the client has filled out the form on the homepage
    if request.method == "POST":
        # Functions and constants used to handle the input values
        UNDEFINED = "-1"
        INFINITY = 100000000
        correct_min = lambda x: 0 if x < 0 else x
        correct_max = lambda x: INFINITY if x < 0 else x

    # Check if the input values are valid or not
    try:
        uni = request.GET.get("uni")
        University.objects.filter(id=uni)[0]
        if uni == "" or uni is None:
            raise ValueError

        rent_min = correct_min(int(request.GET.get("rent_min")))
        rent_max = correct_max(int(request.GET.get("rent_max")))
        distance_min = correct_min(int(request.GET.get("distance_min")))
        distance_max = correct_max(int(request.GET.get("distance_max")))
        crime_rate_max = correct_max(int(request.GET.get("crime_rate_max")))
    except IndexError or ValueError:
        # If the input is invalid
        return render(
            request,
            "best_suburb/400.html",
            {"error_message": "You need to provide a valid uni ID"},
        )
    except TypeError:
        return render(
            request,
            "best_suburb/400.html",
            {"error_message": "You need to provide valid parameters"},
        )

    qualified_suburbs = get_qualified_suburbs(
        uni, rent_min, rent_max, crime_rate_max, distance_min, distance_max
    )

    return JsonResponse(qualified_suburbs)


def list(request):
    """Request handler for the path "/list". This function will
    be called whenever the client requests the path "/list".
    """

    # If this is a GET request, this means the client has filled out the form on the homepage
    # Functions and constants used to handle the input values
    INFINITY = 100000000
    correct_min = lambda x: 0 if x < 0 else x
    correct_max = lambda x: INFINITY if x < 0 else x

    # Check if the input values are valid or not
    try:
        uni = request.GET.get("uni")
        University.objects.filter(id=uni)[0]
        if uni == "" or uni is None:
            raise ValueError

        rent_min = correct_min(int(request.GET.get("rent_min")))
        rent_max = correct_max(int(request.GET.get("rent_max")))
        distance_min = correct_min(int(request.GET.get("distance_min")))
        distance_max = correct_max(int(request.GET.get("distance_max")))
        crime_rate_max = correct_max(int(request.GET.get("crime_rate_max")))
    except IndexError or ValueError:
        # If the input is invalid
        return render(
            request,
            "best_suburb/400.html",
            {"error_message": "You need to provide a valid uni ID"},
        )
    except TypeError:
        return render(
            request,
            "best_suburb/400.html",
            {"error_message": "You need to provide valid parameters"},
        )

    # Save uni into the current session
    request.session["uni"] = uni

    qualified_suburbs = get_qualified_suburbs(
        uni, rent_min, rent_max, crime_rate_max, distance_min, distance_max
    )
    # print("qualixxxxx")
    print(qualified_suburbs)
    # print(qualified_suburbs[1])

    return render(
        request,
        "best_suburb/list.html",
        {
            "suburbs": qualified_suburbs,
            "current_uni": request.session["uni"],
            "universities": University.objects.all(),
        },
    )


def info(request):
    ##1. get the user click suburb
    ##2. serach the suburb name from database
    ##3. display the information of suburb

    # context = {}
    ##now is string,after have database,it need to change it to int

    # context["sub_id"] = primary_key  # get form sql database
    # context["sub_name"] = primary_key  # get form sql database
    # context["sub_postcode"] = "3100"  # get form sql database
    # context["sub_city"] = "Victoria"  # get form sql database
    # context["sub_aver_rent"] = "700"  # get form sql database
    # context["sub_crime_rate"] = "10.2"  # get form sql database
    # context["distance"] = "5"  # get form googlemap
    # context["have_transport"] = "No"  # get form sql database
    # school_name = "Monash"
    # suburbs_name = "Clayton"

    # context["char"] = myechar.render_embed()


    suburb = Suburb.objects.filter(id=request.GET.get("suburb")).values()[0]

    # get the char
    myechar = get_crimerate_char(suburb)
    recome = recom_char()

    average_char = get_average_char(suburb)
    # Add additional attributes to the suburb
    suburb["photos"] = get_photos(request.GET.get("place_id"))
    suburb["distance"] = get_distance(suburb, request.session["uni"])
    
    uni = request.session["uni"]
    university = University.objects.filter(id=uni).values()[0]    
    uni_name = university.get("name")

    return render(
        request,
        "best_suburb/info.html",
        {
            "suburb": convert_coordinates(suburb),
            "uni_name": uni_name,
            "crime_char": myechar.render_embed(),
            "recom_char": recome,
            "average_char":average_char.render_embed(),
        },
    )


def get_crimerate_char(suber_name):
    item_color_js_2 = """new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
                                            offset: 0,
                                            color: 'rgb(129, 227, 238)'
                                        }, {
                                            offset: 1,
                                            color: 'rgb(25, 183, 207)'
                                        }])"""
    x_data = ["2013", "2014", "2015", "2016", "2017", "2018","2019","2020","2021"]
    y_data = [suber_name.get('crime_rate_in_2013'), suber_name.get('crime_rate_in_2014'), suber_name.get('crime_rate_in_2015'),
              suber_name.get('crime_rate_in_2016'), suber_name.get('crime_rate_in_2017'), suber_name.get('crime_rate_in_2018'),
              suber_name.get('crime_rate_in_2019'),suber_name.get('crime_rate_in_2020'),suber_name.get('crime_rate_in_2021')]

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
                title=suber_name.get('name')+" crime rate in ten year", pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(is_show=True, pos_left="70%", pos_bottom="80%"),
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
    x_data = ["2013", "2014", "2015", "2016", "2017", "2018","2019","2020","2021"]
    y_data = [suber_name.get('averagerent_in_2013'), suber_name.get('averagerent_in_2014'), suber_name.get('averagerent_in_2015'),
              suber_name.get('averagerent_in_2016'), suber_name.get('averagerent_in_2017'), suber_name.get('averagerent_in_2018'),
              suber_name.get('averagerent_in_2019'),suber_name.get('averagerent_in_2020'),suber_name.get('averagerent_in_2021')]

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
                title=suber_name.get('name')+" average rent in ten year", pos_left="center"
            ),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            legend_opts=opts.LegendOpts(is_show=True, pos_left="70%", pos_bottom="80%"),
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
    max_crimerate = (Suburb.objects.all().aggregate(Max('crime_rate'))).get('crime_rate__max')
    min_crimerate = (Suburb.objects.all().aggregate(Min('crime_rate'))).get('crime_rate__min')
    max_averagerent = (Suburb.objects.all().aggregate(Max('average_rent'))).get('average_rent__max')
    min_averagerent =( Suburb.objects.all().aggregate(Min('average_rent'))).get('average_rent__min')
    print(max_crimerate)
    print(min_crimerate)
    print(max_averagerent)
    print(min_averagerent)

    return liquid.render_embed()

def recommended_system(qualified_suburbs):

    new_list=[]
    max_crimerate = Suburb.objects.all().aggregate(Max('crime_rate')).get('crime_rate__max')
    min_crimerate = Suburb.objects.all().aggregate(Min('crime_rate')).get('crime_rate__min')
    max_averagerent = Suburb.objects.all().aggregate(Max('average_rent')).get('average_rent__max')
    min_averagerent = Suburb.objects.all().aggregate(Min('average_rent')).get('average_rent__min')


    lenth=len(qualified_suburbs)
    for i in range(0,lenth):
        suburb=qualified_suburbs[i]

    return new_list

def get_suburb_score(suburb,max_crime,min_crime,max_rent,min_rent):
    score=0
    rent=suburb.get('average_rent')
    crime=suburb.get('crime_rate')
    return score