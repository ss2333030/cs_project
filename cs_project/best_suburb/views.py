from http.client import HTTPResponse
from os import lstat
from django.shortcuts import render


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

    context["sub_id"]=primary_key
    context["sub_name"] = primary_key
    context["sub_postcode"] = primary_key
    context["sub_city"] = primary_key
    context["sub_aver_rent"] = primary_key
    context["sub_crime_rate"] = primary_key



    return render(request, "best_suburb/info.html",context)
