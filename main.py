import requests
from weather_scraper import weather_reminder

def get_personal_info(file_path):
    f = open(file_path)
    pushover_api_token = f.readline().strip()
    pushover_api_key = f.readline().strip()
    openweathermap_api_key = f.readline().strip()
    
    return pushover_api_token, pushover_api_key, openweathermap_api_key

def send_message():
    pushover_url = "https://api.pushover.net/1/messages.json"
    
    pushover_api_token, pushover_api_key, openweathermap_api_key = get_personal_info("./Key Information.txt")

    subjects, bodies = weather_reminder(openweathermap_api_key)
    
    if subjects != None and bodies != None:

        for subject, body in zip(subjects, bodies):
            data = {
                "token": pushover_api_token,
                "user": pushover_api_key,
                "message": body,
                "title": subject
            }
            response = requests.post(pushover_url, data=data)

send_message()
