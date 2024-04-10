from django.shortcuts import render,HttpResponse
import json
import requests
from .models import City
from .forms import CityForm

# Create your views here.
def weather(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=11eefc44f15b5ca41f7d54bbbed42445'
    cities = City.objects.all() #return all the cities in the database

    if request.method == 'POST': # only true if form is submitted
        form = CityForm(request.POST) # add actual request data to form for processing
        form.save() # will validate and save if validate

    form = CityForm()
    weather_data = []
    
    for city in cities:

        list_of_data = requests.get(url.format(city)).json() #request the API data and convert the JSON to Python data types

        weather = {
            "city":city,
            "contry_code":str(list_of_data["sys"]["country"]),
            "temp":str(list_of_data["main"]["temp"]),
            "feels_like":str(list_of_data["main"]["feels_like"]),
            "temp_max":list_of_data["main"]["temp_max"],
            "temp_min":list_of_data["main"]["temp_min"],
            "desc":str(list_of_data["weather"][0]["description"]),
            "icon":str(list_of_data["weather"][0]["icon"]),
        }

        weather_data.append(weather) #add the data for the current city into our list

    context = {'weather_data' : weather_data, 'form': form }
    return render(request,"Weather.html",context)