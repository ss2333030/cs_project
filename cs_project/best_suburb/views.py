from http.client import HTTPResponse
from os import lstat
from django.shortcuts import render
from pyecharts import options as opts
from pyecharts.charts import Bar,Line
from pyecharts import options as opts
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.faker import Faker


class Suburb:
    def __init__(self, name, postcode, state, distance, crime_rate, rent):
        self.name = name
        self.postcode = postcode
        self.state = state
        self.distance = distance
        self.crime_rate = crime_rate
        self.rent = rent


suburbs = []
suburbs.append(Suburb("Clayton", "3168", "Victoria", 1, 1, 200))
suburbs.append(Suburb("Malvern East", "3145", "Victoria", 10, 1, 300))
suburbs.append(Suburb("Oakleigh East", "3166", "Victoria", 3, 1, 210))
suburbs.append(Suburb("Caufield", "3150", "Victoria", 7, 1, 200))

# Create your views here.
def index(request):
    return render(request, "best_suburb/index.html")


def list(request):
    if request.method == "POST":

        get_min_value = lambda x: 0 if x == -1 else x
        get_max_value = lambda x: float("inf") if x== -1 else x

        school_name = request.POST.get("school_name")
        distance_min = get_min_value(int(request.POST.get("distance_min"))) 
        distance_max = get_max_value(int(request.POST.get("distance_max")))
        rent_min = get_min_value(int(request.POST.get("rent_min")) )
        rent_max = get_max_value(int(request.POST.get("rent_max")))
        crime_rate_min = get_min_value(int(request.POST.get("crime_rate_min")))
        crimte_rate_max = get_max_value(int(request.POST.get("crime_rate_max")))

        filter = lambda lst, f: lst if len(lst) == 0 else [lst[0]] + filter(lst[1:],f) if f(lst[0]) else filter(lst[1:],f)
        
        qualified_suburbs = filter(suburbs, lambda e: distance_min<=e.distance<=distance_max and rent_min<=e.rent<=rent_max and crime_rate_min<=e.crime_rate<=crimte_rate_max)

        return render(request, "best_suburb/list.html", {"qualified_suburbs": qualified_suburbs})

    return render(request, "best_suburb/list.html"  )


def info(request):
    ##1. get the user click suburb
    ##2. serach the suburb name from database
    ##3. display the information of suburb

    context={}
    ##now is string,after have database,it need to change it to int
    primary_key=request.POST.get("primary_id")

    context["sub_id"]=primary_key      #get form sql database
    context["sub_name"] = primary_key       #get form sql database
    context["sub_postcode"] = "3100"     #get form sql database
    context["sub_city"] = "Victoria"     #get form sql database
    context["sub_aver_rent"] ="700"     #get form sql database
    context["sub_crime_rate"] = "10.2"     #get form sql database
    context["distance"]="5"     #get form googlemap
    context["have_transport"]="No"      #get form sql database
    school_name="Monash"
    suburbs_name="Clayton"

    myechar = get_char()
    context["char"]=myechar.render_embed()


    return render(request, "best_suburb/info.html",context)

def get_char():
    x_data = ["2012", "2014", "2016", "2018", "2020", "2022"]
    y_data = [2,4,6,8,3,4]

    c=(
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
                axislabel_opts=opts.LabelOpts(formatter="{value}%")
            ),
            xaxis_opts=opts.AxisOpts(type_="category",
                                     name="Years",boundary_gap=False),
        )

    )
    return c
