import requests 
import datetime
from datetime import date
from alerts import check_alerts
from clothing_recommender import main_recommendation
import pytz

emojis = {
    "Thunderstorm": "⛈️",
    "Drizzle": "<0xF0><0x9F><0xAB><0x8E>", 
    "Rain": "🌧️",
    "Snow": "❄️",
    "Clear": "☀️",
    "Clouds": "☁️",
    "Mist": "🌫️",
    "Smoke": "💨",
    "Haze": "🌫️",
    "Dust": "💨",
    "Fog": "🌫️",
    "Sand": "",
    "Ash": "",
    "Tornado": "🌪️",
    "Temperature": "🌡️",
    "Feels Cold": "🥶",
    "Feels Hot": "🥵",
    "Humidity": "💧",
    "Visibility": "👁️",
    "Precipitation": "<0xF0><0x9F><0x8C><0x9E>", 
    "Sunrise": "🌅",
    "Sunset": "🌇",
    "Moon": {
        "New Moon": "🌑",
        "Waxing Crescent": "🌒",
        "First Quarter": "🌓",
        "Waxing Gibbous": "🌔",
        "Full Moon": "🌕",
        "Waning Gibbous": "🌖",
        "Third Quarter": "🌗",
        "Waning Crescent": "🌘"
    },
    "Warning": "⚠️",
}

def weather_reminder(api_key):     
    lat = 42.36
    lon = -71.05
    units = "imperial"
    
    openweathermap_url = f"https://api.openweathermap.org/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}&units={units}"
    
    response = requests.get(openweathermap_url)
            
    if response.status_code == 200:
        
        data = response.json()    
        
        current = data["current"]
        
        daily = data["daily"][0]
        
        hourly = data['hourly'][0:12]
        
        curr_date = date.today()
        formatted_date = curr_date.strftime("%Y-%m-%d")
                
        num_messages = 4
        
        alerts = data.get("alerts", [])
        
        alert_responses = None
        
        if alerts:
            alert_responses = check_alerts(alerts)
            num_messages += len(alerts)
            
        subjects = [0] * num_messages
        bodies = [0] * num_messages
        
        clothing = main_recommendation(daily["weather"][0]["main"], daily["temp"]["day"])
        
        subjects[0], bodies[0] = create_report(current, formatted_date)
        subjects[1], bodies[1] = create_daily_report(daily, formatted_date)
        subjects[2], bodies[2] = create_hourly_report(hourly, formatted_date)
        subjects[3], bodies[3] = "Clothing Recommendations", clothing
        
        if alert_responses != None:
            curr_index = 4
            for key in alert_responses:
                subjects[curr_index] = key
                bodies[curr_index] = alert_responses[key]
                curr_index += 1
                        
        return subjects, bodies
    else:
        return None, None
    
def create_report(data, date):
    
    outputs = calculate_outputs(data, True)
    
    subject = f"Current Weather Forecast for {date}"
    
    current_main_weather = data["weather"][0]["main"]
        
    body = f"""        
    Current Weather Report: {outputs["weather"]}
    {emojis[current_main_weather]} Current Weather Type: {current_main_weather}
    {emojis["Temperature"]} Temperature: {data["temp"]}°F (Feels Like: {data["feels_like"]}°F)    
    {emojis["Humidity"]} Humidity: {outputs["humidity"]}
    {emojis["Dust"]} Wind Speed: {outputs["wind_speed"]}
    {emojis["Clouds"]} Cloudiness: {outputs["clouds"]}
    {emojis["Visibility"]} Visibility: {outputs["visibility"]} 
    {emojis["Clear"]} UV Radation: {outputs["uvi"]}
    """
    
    return subject, body

def create_daily_report(daily_data, date):
    daily_outputs = calculate_outputs(daily_data, False)
    
    daily_subject = f"Daily Weather Forecast for {date}"
    
    moonphase_emoji = calculate_moonphase_emoji(daily_data["moon_phase"])

    daily_body = f"""
    Summary: {daily_data["summary"]}
    {emojis["Temperature"]} Temperature: {daily_data["temp"]["day"]}°F 
    Feels Like: {daily_data["feels_like"]["day"]}°F
    High: {daily_data["temp"]["max"]}°F
    Low:  {daily_data["temp"]["min"]}°F
    {emojis["Humidity"]} Humidity: {daily_outputs["humidity"]}
    {emojis["Dust"]} Wind Chill: {calculate_wind_chill(daily_data["temp"]["day"], daily_data["wind_speed"])}
    {emojis["Dust"]} Wind Speed: {daily_outputs["wind_speed"]}
    {emojis["Clouds"]} Cloudiness: {daily_outputs["clouds"]}
    {emojis["Clear"]} UV Radiation: {daily_outputs["uvi"]}
    {emojis["Sunrise"]} Sunrise: {daily_data["sunrise"]}
    {emojis["Sunset"]} Sunset: {daily_data["sunset"]}
    {emojis["Moon"][moonphase_emoji]} {moonphase_emoji}
    """
    
    return daily_subject, daily_body

def create_hourly_report(hourly_data, date):
    hourly_outputs = calculate_hourly_outputs(hourly_data)
    
    hourly_subject = f"Hourly Weather Forecast for {date}"
    
    hourly_body = ""
        
    for key in hourly_outputs:
        hourly_body += f"{hourly_outputs[key][0]}°F (Feels Like: {hourly_outputs[key][1]}°F)"
        hourly_body += f"\n{hourly_outputs[key][2]}\n"
        
    return hourly_subject, hourly_body
    
def calculate_hourly_outputs(data_dic):
    output_dic = {}
    
    for data in data_dic:
        time = get_time(data["dt"])
        output_dic[time] = []
        output_dic[time].append(data["temp"])
        output_dic[time].append(data["feels_like"])
        precipitation_probability = calculate_precipitation(data)
        output_dic[time].append(precipitation_probability)
        
    return output_dic
    
def calculate_outputs(data_dic, is_current):
    output_dic = {}
    output_dic["humidity"] = humidity_response(data_dic["humidity"])
    output_dic["wind_speed"] = wind_speed_response(data_dic["wind_speed"])
    output_dic["uvi"] = uvi_response(data_dic["uvi"])
    output_dic["clouds"] = cloudiness_response(data_dic["clouds"])
    if is_current:
        output_dic["visibility"] = visibility_response(data_dic["visibility"])
        output_dic["weather"] = main_weather(data_dic["weather"][0]["main"], data_dic["weather"][0]["description"])
    else:
        output_dic["precipitation"] = calculate_precipitation(data_dic)
    return output_dic

def calculate_precipitation(data_dic):
    if "rain" in data_dic.values():
        return f"Chance of Rain: {data_dic["pop"]} (Depth: {data_dic["rain"]} mm)"
    
    elif "snow" in data_dic.values():
        return f"Chance of Snow: {data_dic["pop"]} (Depth: {data_dic["snow"]} mm)"
    
    else:
        return f"Chance of Precipitation: {data_dic["pop"] * 10}%"
    

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
    
def uvi_response(uvi):
    if uvi >= 11:
        return "Extremely High"
    elif uvi >= 8 and uvi < 11:
        return "Very High"
    elif uvi >= 6 and uvi < 8:
        return "High"
    elif uvi >= 3 and uvi < 6:
        return "Normal"
    else:
        return "Low"
    
def cloudiness_response(cloudiness):
    if cloudiness >= 90:
        return "Extremely Cloudy"
    elif cloudiness < 90 and cloudiness >= 75:
        return "Very Cloudy"
    elif cloudiness < 75 and cloudiness >= 50:
        return "Cloudy"
    elif cloudiness < 50 and cloudiness >= 25:
        return "Slightly Cloudy"
    elif cloudiness < 25 and cloudiness >= 5:
        return "Not Cloudy"
    else:
        return "No Clouds"

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
        
def calculate_wind_chill(temp, wind_speed):
    if (temp <= 50 and wind_speed > 3):
        wind_chill = 35.74 + (0.6215 * temp) - (35.75 * (wind_speed ** 0.16)) + (0.4275 * temp * (wind_speed ** 0.16))
        return round(wind_chill, 2)
    else:
        return "No wind chill"
    
def get_time(dt):
    est_timezone = pytz.timezone('US/Eastern')
    utc_datetime_object = datetime.datetime.fromtimestamp(dt, tz=pytz.utc)
    est_datetime_object = utc_datetime_object.astimezone(est_timezone)
    time = est_datetime_object.strftime("%H:%M:%S")
    
    return time

def calculate_moonphase_emoji(phase_num):
    if phase_num == 0 or phase_num == 1:
        return "New Moon"
    elif phase_num > 0 and phase_num < 0.25:
        return "Waxing Crescent"
    elif phase_num == 0.25:
        return "First Quarter"
    elif phase_num > 0.25 and phase_num < 0.5:
        return "Waxing Gibbous"
    elif phase_num == 0.5:
        return "Full Moon"
    elif phase_num > 0.5 and phase_num < 0.75:
        return "Waning Gibbous"
    elif phase_num == 0.75:
        return "Third Quarter"
    else:
        return "Waning Crescent"
