import schedule 
import smtplib 
import requests 
from bs4 import BeautifulSoup 
import os
from datetime import date


def weather_reminder(api_key): 
    
    city = "Boston"
    
    openweathermap_url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'

    response = requests.get(openweathermap_url)
    
    username = "Andrew Thynne"
    
    # Add code to deal with different response statuses
    if response.status_code == 200:
        data = response.json()
        curr_temp = kelvin_to_fahrenheit(data["main"]["temp"])
        perceived_temp = kelvin_to_fahrenheit(data["main"]["feels_like"])
        max_temp = kelvin_to_fahrenheit(data["main"]["temp_max"])
        min_temp = kelvin_to_fahrenheit(data["main"]["temp_min"])
        weather = data["weather"][0]["main"]
        weather_desc = data["weather"][0]["description"]    
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]
        # Measured in hpa
        pressure = data["main"]["pressure"]
        visibility = data["visibility"]
        
        curr_date = date.today()
        
        weather_output = main_weather(weather, weather_desc)
        
        humidity_output = humidity_response(humidity)
        
        wind_speed_output = wind_speed_response(wind_speed)
        
        visibility_output = visibility_response(visibility)
        
        # switch curr_temp with mean temp
        clothing = clothing_recommendation(weather, curr_temp)
        
        formatted_date = curr_date.strftime("%Y-%m-%d")
        
        subject = f"Weather Reminder for {formatted_date}"
        
        body = f"""
        Dear {username},
        
        {weather_output}
        
        Current Temperature: {curr_temp}
        Feels Like: {perceived_temp}
        High: {max_temp}
        Low: {min_temp}
        
        Clothing Recommendation: {clothing}
        
        Humidity: {humidity_output}
        
        Wind Speed: {wind_speed_output}
        
        Visibility: {visibility_output}
        """
                
        return subject, body
    else:
        return "nothing"
  
def get_requests(city):
    # creating url and requests instance 
	url = "https://www.google.com/search?q=" + "weather" + city 
	html = requests.get(url).content
 
def kelvin_to_fahrenheit(temp):
    fahrenheit = (temp - 273.15) * 1.8 + 32
    return round(fahrenheit, 2)

def humidity_response(humidity):
    if humidity >= 60 and humidity < 80:
        return "High"
    
    elif humidity >= 80:
        return "Very High"
    
    elif humidity >= 30 and humidity < 50:
        return "Normal"
    
    elif humidity >= 50 and humidity < 60:
        return "Slightly High"
    
    elif humidity >= 15 and humidity < 30:
        return "Low"
    
    else:
        return "Very Low"

def wind_speed_response(wind_speed):
    wind_speed = round(wind_speed * 2.2369, 2)
    
    if wind_speed >= 57:
        return "Dangerously Windy"
    
    elif wind_speed >= 40 and wind_speed < 57:
        return "Very Windy"
    
    elif wind_speed >= 26 and wind_speed < 40:
        return "Windy"
    
    else:
        return "Not Windy"

def visibility_response(visibility):
    if visibility < 1001:
        return "Very Poor"
    elif visibility >= 1001 and visibility < 4001:
        return "Poor"
    elif visibility >= 4001 and visibility < 10001: 
        return "Moderate"
    elif visibility >= 10001 and visibility < 20001:
        return "Good"
    else:
        return "Very Good"

def desc_weather_thunderstorm(desc):
    thunderstorm_dic = {
        "thunderstorm with light rain": "Stays indoors to avoid the thunderstorm, but wear a raincoat or other waterproof gear if you go outside.",
        "thunderstorm with rain": "Stay indoors to avoid the thunderstorm, but wear a heavy raincoat if you go outside.",
        "thunderstorm with heavy rain": "Stay inside, away from heavy rain and potential lightning strikes.",
        "light thunderstorm": "Be cautious if you're outside, as lightning and rain may be present.",
        "thunderstorm": "Stay indoors to avoid the dangers of the thunderstorm.",
        "heavy thunderstorm": "WARNING: Do not go outside. This is a dangerous thunderstorm with strong winds and lightning.",
        "ragged thunderstorm": "Irregular thunderstorms can be unpredictable. Stay safe and avoid going outside.",
        "thunderstorm with light drizzle": "A light drizzle with thunder may not seem bad, but stay aware of potential lightning.",
        "thunderstorm with drizzle": "Drizzle combined with thunderstorms can still be hazardous. Stay indoors if possible.",
        "thunderstorm with heavy drizzle": "Stay inside to avoid the thunderstorm, but wear waterproof gear or a raincoat if you go outside"
    }
    
    return thunderstorm_dic[desc]

def desc_weather_drizzle(desc):
    drizzle_dic = {
        "light intensity drizzle": "A light drizzle is falling. A light jacket or umbrella should be enough.",
        "drizzle": "It's drizzling. If heading out, wear a raincoat or carry an umbrella.",
        "heavy intensity drizzle": "This is a strong drizzle, almost rain-like. Consider waterproof clothing.",
        "light intensity drizzle rain": "A combination of drizzle and light rain. You might need an umbrella or a hooded jacket.",
        "drizzle rain": "A steady drizzle mixed with rain. It’s best to wear waterproof clothing if going outside.",
        "heavy intensity drizzle rain": "Heavy drizzle and rain can make surfaces slippery. Be cautious when walking or driving.",
        "shower rain and drizzle": "Intermittent rain and drizzle. Keep an umbrella handy.",
        "heavy shower rain and drizzle": "Sudden bursts of rain mixed with drizzle. You might want to avoid going outside.",
        "shower drizzle": "Drizzle showers come and go. Be prepared for brief wet conditions."
    }
    
    return drizzle_dic[desc]
    
def desc_weather_rain(desc):
    rain_dic = {
        "light rain": "A light rain is falling. A small umbrella or hooded jacket should suffice.",
        "moderate rain": "A steady rain. Waterproof clothing is recommended.",
        "heavy intensity rain": "The rain is strong. Avoid unnecessary outdoor activities if possible.",
        "very heavy rain": "Very heavy rainfall can cause visibility issues and flooding. Stay indoors if possible.",
        "extreme rain": "WARNING: Extreme rain could lead to flash flooding. Avoid travel.",
        "freezing rain": "Hazardous freezing rain is occurring. Roads and sidewalks may be icy—stay inside if possible.",
        "light intensity shower rain": "Intermittent light rain showers. Carrying an umbrella is a good idea.",
        "shower rain": "Scattered rain showers. Be prepared for sudden wet conditions.",
        "heavy intensity shower rain": "Heavy rain showers can create slippery roads and reduced visibility. Be cautious.",
        "ragged shower rain": "Unpredictable rain showers. Keep an umbrella with you if going out."
    }
    
    return rain_dic[desc]
    
def desc_weather_clouds(desc):   
    clouds_dic = {
        "few clouds": "A few clouds in the sky, but overall, it's a nice day.",
        "scattered clouds": "Some scattered clouds. Expect partial sunshine throughout the day.",
        "broken clouds": "Cloud coverage is significant, but you might still see some sun.",
        "overcast clouds": "The sky is fully covered with clouds. It may feel gloomy or lead to rain."
    }
    
    return clouds_dic[desc]
    
def desc_weather_snow(desc):
    snow_dic = {
        "light snow": "Light snowfall. Roads may be slightly slippery, so be cautious.",
        "snow": "Snowfall is occurring. Dress warmly and watch for icy conditions.",
        "heavy snow": "Heavy snow is falling. Travel may be difficult—stay indoors if possible.",
        "sleet": "Sleet is falling. This can create dangerous icy conditions—exercise caution.",
        "light shower sleet": "Light sleet showers. Surfaces may become icy, so tread carefully.",
        "shower sleet": "Intermittent sleet showers. Roads and sidewalks could be hazardous.",
        "light rain and snow": "A mix of rain and snow. It might be slushy outside—wear waterproof footwear.",
        "rain and snow": "Rain mixed with snow. Roads may be slippery, so drive carefully.",
        "light shower snow": "Scattered light snow showers. No major accumulation expected.",
        "shower snow": "Intermittent snow showers. Be prepared for sudden snowfall.",
        "heavy shower snow": "Intense bursts of snow. Visibility may drop—avoid driving if possible."
    }
    
    return snow_dic[desc]

def main_weather(weather, weather_desc):
    if weather == "Thunderstorm":
        
        return desc_weather_thunderstorm(weather_desc)
        
    elif weather == "Drizzle":
        
        return desc_weather_drizzle(weather_desc)
        
    elif weather == "Rain":
        
        return desc_weather_rain(weather_desc)
    
    elif weather == "Snow":
        
        return desc_weather_snow(weather_desc)
        
    elif weather == "Clear":
        
        return "Clear skies, enjoy the view."
    
    elif weather == "Clouds":
        
        return desc_weather_clouds(weather_desc)
        
    else:
        
        if weather == "Mist":
            
            return "Misty outside. Be careful when driving."
            
        elif weather == "Smoke":
            
            return "Low visibility outside due to smoke. Try to stay inside."
            
        elif weather == "Haze":
            
            return "Haze outside. Be careful when driving."
            
        elif weather == "Dust":
            
            if weather_desc == "sand/dust whirls":
                
                return "Dusty outside. Wear eye protection and keep your mouth covered"
            
            else:
                
                return "Somewhat dusty outside."
                
        elif weather == "Fog":
            
            return "Foggy outside. Be careful when driving."
            
        elif weather == "Sand":
            
            return "Sandy outside. Make sure to cover your mouth and wear eye protection."
            
        elif weather == "Ash":
            
            return "WARNING: Ash outside. Stay indoors and close all doors and windows."
            
        elif weather == "Squall":
            
            return "WARNING: Potential storm that will last for a couple of minutes. Don't do anything outdoors for too long."
        
        else:
            return "WARNING: Tornado. Stay inside a sturdy shelter and go to its lowest level."
    
def clothing_recommendation(weather, temp):
    if weather == "Rain" or weather == "Drizzle" or weather == "Thundestorm":
        return "Raincoat or waterproof clothing"
    elif weather == "Snow":
        return "Heavy insulated jacket and pants"
    else:
        if temp < 20:
            return "Heavy insulated jacket and multiple layers underneath"
        elif temp <= 20 and temp < 40:
            return "Heavy jacket and pants"
        elif temp <= 40 and temp < 60:
            return "Jacket and pants"
        elif temp <= 60 and temp < 75:
            return "Light jacket or long sleeve shirt and shorts"
        else:
            return "Short sleeve shirt and shorts"
        
    


