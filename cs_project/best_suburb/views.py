from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django import forms

class NewForm(forms.Form):
    task = forms.CharField(label="New Task")


class Suburb:
    def __init__(self, name, postcode, state, distance, crime_rate, average_rent):
        self.name = name
        self.postcode = postcode
        self.state = state
        self.distance = distance
        self.crime_rate = crime_rate
        self.average_rent = average_rent


suburbs = []
suburbs.append(Suburb("Clayton", "3168", "Victoria", 1, 1, 200))
suburbs.append(Suburb("Malvern East", "3145", "Victoria", 10, 1, 300))
suburbs.append(Suburb("Oakleigh East", "3166", "Victoria", 3, 1, 210))
suburbs.append(Suburb("Caufield", "3150", "Victoria", 7, 1, 200))

# Create your views here.

# def index(request):
#     return HttpResponse("<h1 style=\"color:blue\">Hello, world!</h1>")
def index(request):
    return render(request, "best_suburb/index.html")


def list(request):
    return render(request, "best_suburb/list.html")

def info(request):
    return render(request, "best_suburb/info.html")