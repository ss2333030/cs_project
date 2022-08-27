from ast import Sub
from http.client import HTTPResponse
import imp
from os import lstat
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker
from django.http import JsonResponse
from .models import Suburb,University
from best_suburb import models
from django.shortcuts import render,HttpResponse

def addUni(request):
    University = models.University(name="MMM",suburbname="Sname",location = "33,33")
    University.save()
    return HttpResponse("<p>Success<p>")

def search():
    PrintSuburb = models.Suburb.objects.all()
    for i in PrintSuburb:
        print(i.crime_rate)
    return 0

s1 = {
    "name": "Clayton",
    "postcode": "3168",
    "state": "Victoria",
    "distance": 1,
    "crime_rate": 1,
    "rent": 200,
}
s2 = {
    "name": "Malvern East",
    "postcode": "3145",
    "Victoria": "Victoria",
    "distance": 10,
    "crime_rate": 1,
    "rent": 300,
}
s3 = {
    "name": "Oakleigh East",
    "postcode": "3166",
    "Victoria": "Victoria",
    "distance": 3,
    "crime_rate": 1,
    "rent": 210,
}
s4 = {
    "name": "Caufield",
    "postcode": "3150",
    "state": "Victoria",
    "distance": 7,
    "crime_rate": 1,
    "rent": 200,
}

suburbs = []
suburbs.append(s1)
suburbs.append(s2)
suburbs.append(s3)
suburbs.append(s4)


# Create your views here.


def index(request):
    """Request handler for the path "/". This function will be called whenever the client requests the path "/"."""

    # This returns the page "index.html"

    return render(request, "best_suburb/index.html")


def list(request):
    #search()
    """Request handler for the path "/list". This function will be called whenever the client requests the path "/list"."""
    if request.method == "POST":
        return render(
            request,
            "best_suburb/list.html",
            {"suburbs": get_qualified_suburbs(request)},
        )

    # if the client accesses this path directly without filling the form, send all suburbs to the client
    return render(request, "best_suburb/list.html", {"suburbs": suburbs})


def get_qualified_suburbs(request):
    """Returns the correct result according to user input."""

    # if the client has filled out the form on the homepage
    # Functions used to convert the input value to its correct value
    UNDEFINED = "-1"

    correct_value = lambda value: UNDEFINED if value is None or value == "" else value
    correct_min = lambda x: 0 if x < 0 else x
    correct_max = lambda x: float("inf") if x < 0 else x

    # Get the values
    uni_name = correct_value(request.POST.get("uni_name"))
    distance_min = correct_min(int(correct_value(request.POST.get("distance_min"))))
    distance_max = correct_max(int(correct_value(request.POST.get("distance_max"))))
    rent_min = correct_min(int(correct_value(request.POST.get("rent_min"))))
    rent_max = correct_max(int(correct_value(request.POST.get("rent_max"))))
    crime_rate_min = correct_min(int(correct_value(request.POST.get("crime_rate_min"))))
    crimte_rate_max = correct_max(
        int(correct_value(request.POST.get("crime_rate_max")))
    )

    # Function used to filter out unqualified suburbs
    filter = (
        lambda lst, f: lst
        if len(lst) == 0
        else ([lst[0]] + filter(lst[1:], f) if f(lst[0]) else filter(lst[1:], f))
    )

    return filter(
        suburbs,
        lambda e: distance_min <= e["distance"] <= distance_max
        and rent_min <= e["rent"] <= rent_max
        and crime_rate_min <= e["crime_rate"] <= crimte_rate_max,
    )


def info(request):
    ##1. get the user click suburb
    ##2. serach the suburb name from database
    ##3. display the information of suburb

    context = {}
    ##now is string,after have database,it need to change it to int
    primary_key = request.POST.get("primary_id")

    context["sub_id"] = primary_key  # get form sql database
    context["sub_name"] = primary_key  # get form sql database
    context["sub_postcode"] = "3100"  # get form sql database
    context["sub_city"] = "Victoria"  # get form sql database
    context["sub_aver_rent"] = "700"  # get form sql database
    context["sub_crime_rate"] = "10.2"  # get form sql database
    context["distance"] = "5"  # get form googlemap
    context["have_transport"] = "No"  # get form sql database
    school_name = "Monash"
    suburbs_name = "Clayton"

    myechar = get_char()
    context["char"] = myechar.render_embed()

    return render(request, "best_suburb/info.html", context)


def get_char():
    x_data = ["2012", "2014", "2016", "2018", "2020", "2022"]
    y_data = [2, 4, 6, 8, 3, 4]

    c = (
        Line()
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
