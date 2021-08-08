from tkinter import ttk
from tkinter import font
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import requests
import io
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

    weatherOptions = Frame(root)

    refreshingOptions = Frame(root)

    #app grid
    cityName.grid(row=0, column=0, sticky="nsew")
    weatherImage.grid(row=1, column=0, sticky="nsew")
    weatherInfo.grid(row=2, column=0, columnspan=3, sticky="nsew")
    weatherOptions.grid(row=3, column=0, sticky="nsew")
    refreshingOptions.grid(row=4, column=0, sticky="nsew")

    #weather info grid
    weatherInfo.columnconfigure((0,1,2), weight=1)
    weatherInfo.rowconfigure((0,1), weight=1)

    #weather options grid

    weatherOptions.columnconfigure((0,1,2,3,4,5), weight=1)
    weatherOptions.rowconfigure(0, weight=1)
    weatherOptions.rowconfigure(1, weight=3)

    Label(weatherOptions, text="Choose own units", anchor="e", justify=LEFT).grid(row=0, column=0, columnspan=10)

    #weather options vars

    tempUnit = StringVar()
    tempUnit.set("Celsius")

    windSpeedUnit = StringVar()
    windSpeedUnit.set("Km/h")

    visibilityUnit = StringVar()
    visibilityUnit.set("Kilometers")

    #weather info data

    def updateInfos():

        settings = [tempUnit, windSpeedUnit]

        tempInfo = StringVar()
        feelTempInfo = StringVar()
        windSpeedInfo = StringVar()
        visibilityInfo = (str(actualWeather['current']['vis_km']))
        windDirInfo = (str(actualWeather['current']['wind_dir']))
        pressureInfo = (str(actualWeather['current']['pressure_mb']))

        for x in settings:
            if x.get() == "Celsius":
                tempInfo.set(str(actualWeather['current']['temp_c']) + " C°")
                feelTempInfo.set(str(actualWeather['current']['feelslike_c']) + " C°")
            if x.get() == "Fahrenheit":
                tempInfo.set(str(actualWeather['current']['temp_f']) + " F°")
                feelTempInfo.set(str(actualWeather['current']['feelslike_f']) + " F°")
            if x.get() == "Km/h":
                windSpeedInfo.set(str(actualWeather['current']['wind_kph']) + " Km/h")
            if x.get() == "Miles/h":
                windSpeedInfo.set(str(actualWeather['current']['wind_mph']) + " Miles/h")

        temp = Label(weatherInfo, text="Temperature: " + tempInfo.get())
        feelTemp = Label(weatherInfo, text="Feel like temperature: " + feelTempInfo.get())
        windSpeed = Label(weatherInfo, text="Wind speed: " + windSpeedInfo.get())
        visibility = Label(weatherInfo, text="Visibility: " + visibilityInfo)
        windDir = Label(weatherInfo, text="Wind direction: " + windDirInfo)
        pressure = Label(weatherInfo, text="Pressure: " + pressureInfo)

        weatherInfo.update_idletasks()

        temp.grid(row=0,column=0)
        feelTemp.grid(row=1,column=0)
        windSpeed.grid(row=0, column=1)
        windDir.grid(row=1, column=1)
        pressure.grid(row=0, column=2)
        visibility.grid(row=1, column=2)
    
    #weather info buttons

    Radiobutton(weatherOptions, text="C°", variable=tempUnit, value="Celsius", command=updateInfos).grid(row=1, column=0)
    Radiobutton(weatherOptions, text="F°", variable=tempUnit, value="Fahrenheit", command=updateInfos).grid(row=1, column=1)

    Radiobutton(weatherOptions, text="Km/h", variable=windSpeedUnit, value="Km/h", command=updateInfos).grid(row=1, column=2)
    Radiobutton(weatherOptions, text="Miles/h", variable=windSpeedUnit, value="Miles/h", command=updateInfos).grid(row=1, column=3)
    """
    Radiobutton(weatherOptions, text="Kilometers", variable=visibilityUnit, value="Kilometers", command=updateInfos).grid(row=1, column=4)
    Radiobutton(weatherOptions, text="Miles", variable=visibilityUnit, value="Miles", command=updateInfos).grid(row=1, column=5)
    """
    updateInfos()
    
    #refresh option 

    def refresh():

        messagebox.showinfo("Refreshed", "Now you have the newest weather info!")

        App()

    refreshingOptions.columnconfigure((0,1), weight=1)

    lastUpdateInfo = actualWeather['current']['last_updated']

    lastUpdate = Label(refreshingOptions, text="Last updated: " + str(lastUpdateInfo))
    refreshButton = Button(refreshingOptions, text="Refresh", command=refresh)

    lastUpdate.grid(column=0, sticky="s")
    refreshButton.grid(column=1)

    #cosmetic changes as font

    cityName.configure(font=('',50), anchor="center")

    weatherImage.configure(anchor="center")
    #mainloop
    root.mainloop()

if __name__ == "__main__":

    #window settings
    root = Tk(className='WeatherApp')
    rootX = "600"
    rootY = "400"
    root.geometry(rootX + "x" + rootY)
    root.columnconfigure((0), weight=1)
    root.rowconfigure((0,2,3,4), weight=1)
    root.rowconfigure(1, weight=4)

    App()
    



