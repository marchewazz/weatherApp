from tkinter import ttk
from tkinter import font
import requests
import io
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
from urllib.request import urlopen
import os

apiKey = os.environ.get('API_KEY')

def getLocation():
    url = "https://ip-geo-location.p.rapidapi.com/ip/check"

    querystring = {"format":"json"}

    headers = {
        'x-rapidapi-key': apiKey,
        'x-rapidapi-host': "ip-geo-location.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    
    return response['city']['name']

def getWeather():
    
    location = getLocation()

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q":location}

    headers = {
        'x-rapidapi-key': apiKey,
        'x-rapidapi-host': "weatherapi-com.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = response.json()
    
    return response

def App():

    #window settings
    root = Tk(className='WeatherApp')
    rootX = "600"
    rootY = "400"
    root.geometry(rootX + "x" + rootY)
    root.columnconfigure((0), weight=1)
    root.rowconfigure((0,2), weight=1)
    root.rowconfigure(1, weight=4)

    #getting weather

    actualWeather = getWeather()


    #getting weather image
    
    url = actualWeather['current']['condition']['icon']

    page = urlopen('http:' + url)

    weatherByteImg = io.BytesIO(page.read())

    weatherPilImg = Image.open(weatherByteImg)

    weatherTkImg = ImageTk.PhotoImage(weatherPilImg)
    
    #app components
    cityName = Label(root, text=actualWeather['location']['name'], justify='right')

    weatherImage = Label(root, image=weatherTkImg)
    
    weatherInfo = Frame(root)

    #app grid
    cityName.grid(row=0, column=0, sticky="nsew")
    weatherImage.grid(row=1, column=0, sticky="nsew")
    weatherInfo.grid(row=2, column=0, columnspan=3, sticky="nsew")

    #weather info grid
    weatherInfo.columnconfigure((0,1,2), weight=1)
    weatherInfo.rowconfigure((0,1), weight=1)

    temp = Label(weatherInfo,text="Temperature: " + str(actualWeather['current']['temp_c']))
    temp.grid(row=0,column=0)

    feelTemp = Label(weatherInfo, text="Feel like temperature: " + str(actualWeather['current']['feelslike_c']))
    feelTemp.grid(row=1,column=0)

    windSpeed = Label(weatherInfo, text="Wind speed: " + str(actualWeather['current']['wind_kph']))
    windSpeed.grid(row=0, column=1)

    windDir = Label(weatherInfo, text="Wind direction: " + str(actualWeather['current']['wind_dir']))
    windDir.grid(row=1, column=1)

    pressure = Label(weatherInfo, text="Pressure: " + str(actualWeather['current']['pressure_mb']))
    pressure.grid(row=0, column=2)

    visibility = Label(weatherInfo, text="Visibility: " + str(actualWeather['current']['vis_km']))
    visibility.grid(row=1, column=2)

    #cosmetic changes as font

    cityName.configure(font=('',50), anchor="center")

    weatherImage.configure(anchor="center")

    #mainloop
    root.mainloop()

if __name__ == "__main__":
    App()
    



