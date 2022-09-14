from ast import Sub
from http.client import HTTPResponse
import imp
from multiprocessing.sharedctypes import Value
from os import lstat
from re import T
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
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
def filter(lst: List[T], f: Callable[[T], bool]):
    return lst if len(lst) == 0 else ([lst[0]] + filter(lst[1:], f) if f(lst[0]) else filter(lst[1:], f))
    

def map(lst: List[T], f:Callable[[T], U]):
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


def get_qualified_suburbs(uni_name: str, rent_min: int, rent_max: int, crime_rate_max: int, distance_min: int, distance_max: int):
    """ Returns the correct suburbs according to user input. """

    # Get the university
    university = University.objects.filter(name=uni_name)[0]

    # Get the list of qualified suburbs
    suburbs = Suburb.objects.filter(
        average_rent__gte=rent_min,
        average_rent__lte=rent_max,
        crime_rate__lte=crime_rate_max
    ).values()


    # Filter suburbs by distance
    def condition(e: Suburb):
        l1 = Location(float(e["latitude"]), float(e["longitude"]))
        l2 = Location(float(university.latitude), float(university.longitude))
        return distance_min <= haversine_distance(l1, l2) <= distance_max

    # Add a distance property to the suburbs
    def add_distance_property(e: Suburb):
        l1 = Location(float(e["latitude"]), float(e["longitude"]))
        l2 = Location(float(university.latitude), float(university.longitude))
        e["distance"] = round(haversine_distance(l1, l2), 2)
        return e

    return map(filter(suburbs, condition), add_distance_property)

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


################################### Views #######################################################
def places(request):
    """ Request handler for getting a list of places."""

    URL = "https://maps.googleapis.com/maps/api/place/autocomplete/json?input=" + request.GET.get("place") +"&key=AIzaSyDRsqK_7w_eBkmNJZUczRnyC9jJx5gj5xQ"
    payload={}
    headers = {}
    response = requests.request("GET", URL, headers=headers, data=payload).json()
    return JsonResponse(response)

# Client -> Server -> Google map API


def index(request):
    """Request handler for the path "/". This function will be 
        called whenever the client requests the path "/".
    """

    # This returns the page "index.html"
    return render(request, "best_suburb/index.html")

def suburbs(request):
    """ Request handler for the path "/suburbs". This function will 
        be called whenever the client requests the path "/suburbs".
    """

    # If this is a GET request, this means the client has filled out the form on the homepage
    # Functions and constants used to handle the input values
    UNDEFINED = "-1"
    INFINITY = 100000000
    correct_min = lambda x: 0 if x < 0 else x
    correct_max = lambda x: INFINITY if x < 0 else x

    # Check if the input values are valid or not
    try:
        uni_name = request.POST.get("uni_name")
        rent_min = correct_min(int(request.POST.get("rent_min")))
        rent_max = correct_max(int(request.POST.get("rent_max")))
        distance_min = correct_min(int(request.POST.get("distance_min")))
        distance_max = correct_max(int(request.POST.get("distance_max")))
        crime_rate_max = correct_max(int(request.POST.get("crime_rate_max")))
    except Exception:
        # If the input is invalid
        return render(request, "best_suburb/400.html")

    # Save uni_name into the current session
    request.session["uni_name"] = uni_name
        
    qualified_suburbs = get_qualified_suburbs(uni_name, rent_min, rent_max, crime_rate_max, distance_min, distance_max)
    return JsonResponse(qualified_suburbs)


def list(request):
    """ Request handler for the path "/list". This function will 
        be called whenever the client requests the path "/list".
    """

    # If this is a GET request, this means the client has filled out the form on the homepage
    # Functions and constants used to handle the input values
    UNDEFINED = "-1"
    INFINITY = 100000000
    correct_min = lambda x: 0 if x < 0 else x
    correct_max = lambda x: INFINITY if x < 0 else x

    # Check if the input values are valid or not
    try:
        uni_name = request.POST.get("uni_name")
        rent_min = correct_min(int(request.POST.get("rent_min")))
        rent_max = correct_max(int(request.POST.get("rent_max")))
        distance_min = correct_min(int(request.POST.get("distance_min")))
        distance_max = correct_max(int(request.POST.get("distance_max")))
        crime_rate_max = correct_max(int(request.POST.get("crime_rate_max")))
    except Exception:
        # If the input is invalid
        return render(request, "best_suburb/400.html")

    # Save uni_name into the current session
    request.session["uni_name"] = uni_name
        
    qualified_suburbs = get_qualified_suburbs(uni_name, rent_min, rent_max, crime_rate_max, distance_min, distance_max)
    return render(request, "best_suburb/list.html", { "suburbs": qualified_suburbs, "uni_name": request.session["uni_name"]})


    # # if the client accesses this path directly without filling the form, send all suburbs to the client
    # return render(request, "best_suburb/list.html", { "suburbs" : Suburb.objects.all().values()})





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
    myechar = get_char()
    print("xxxx")
    print(myechar)
    print("aaaaa")
    return render(
        request,
        "best_suburb/info.html",
        {
            "suburb": convert_coordinates(Suburb.objects.filter(name=request.GET.get("name")).values()[0]),
            "char": myechar.render_embed(),
        },
    )


def get_char():
    x_data = ["2012", "2014", "2016", "2018", "2020", "2022"]
    y_data = [2, 4, 6, 8, 3, 4]

    c = (
        Line(init_opts=opts.InitOpts(width="750px", height="400px"))
        .add_xaxis(xaxis_data=x_data)
        .add_yaxis(
            series_name="Clayton crime rate",
            stack="total",
            y_axis=y_data,
            label_opts=opts.LabelOpts(is_show=False),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(title="   Clayton crime rate in ten year"),
            tooltip_opts=opts.TooltipOpts(trigger="axis"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                name="Crime rate(Percentage%)",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(formatter="{value}%"),
            ),
            xaxis_opts=opts.AxisOpts(
                type_="category", name="Years", boundary_gap=False
            ),
        )
    )
    return c
