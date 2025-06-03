# Weather-Alert-System

# Smart Weather Companion

This Python program provides comprehensive weather information, personalized recommendations, and temperature predictions, delivered daily at 7:00 AM.

## Overview

This project integrates several functionalities to provide a smart weather experience:

* **Detailed Weather Reports:** Retrieves and formats current, daily, and hourly weather information.
* **Categorical Conversion:** Converts numerical weather values (like UVI index and humidity) into descriptive categories (e.g., low, medium, high).
* **Wind Chill Calculation:** Calculates the perceived temperature based on actual temperature and wind speed.
* **Basic Clothing Recommendation:** Suggests clothing items based on the current weather conditions and a user-defined wardrobe.
* **Custom Weather Messages:** Generates personalized messages based on the prevailing weather.
* **LSTM Temperature Prediction:** Utilizes a trained Long Short-Term Memory (LSTM) model to predict future temperatures based on historical weather data. This model boasts high accuracy.
* **Automated Daily Execution:** Configured to run automatically every day at 7:00 AM using Task Scheduler.

## Features

* Provides current weather details (temperature, precipitation, wind, etc.).
* Offers a summary of the daily weather forecast.
* Presents a breakdown of the hourly weather forecast.
* Calculates and displays the wind chill temperature.
* Categorizes the UVI index (e.g., Low, Moderate, High, Very High, Extreme).
* Categorizes humidity levels (e.g., Low, Medium, High).
* Recommends clothing items from a user-defined wardrobe suitable for the current weather.
* Generates a custom message (e.g., "Enjoy the sunny day!", "Don't forget your umbrella!").
* Predicts the temperature using a highly accurate LSTM model.
* Set it up as an executable to run automatically every morning at 7:00 AM, delivering timely information.

## Technologies Used

* Python
* Visual Studio Code
* Task Scheduler
* Keras

## Setup and Installation

1.  **Prerequisites:**
    * Python 3.x installed on your system.
    * Task Scheduler
    * IDE that can run python
    * Install keras, datetime, pytz, and requests
    * Pushover API Key
    * Pushover API Token
    * OpenWeatherMap 3.0 API Key

2.  **Installation:**
    ```bash
    git clone [repository URL]
    cd [repository directory]
    pip install -r requirements.txt
    ```

3.  **Configuration:**
    * **API Keys:** Store your weather API key(s) in the "Key Information" file.
    * **Wardrobe:** Define your wardrobe in wardrobe dictionary
    * **LSTM Model:** Ensure the trained LSTM model file model.keras is in the correct directory.
    * **Task Scheduler:** This program is designed to run via Task Scheduler (on Windows). You will need to configure a task to execute the main script (main.py) daily at 7:00 AM.

## Usage

This program is designed for automated daily execution. Once configured in Task Scheduler, you do not need to manually run it. The program will:

1.  Fetch the latest weather data.
2.  Process the data, including calculations and categorizations.
3.  Generate a clothing recommendation based on your wardrobe.
4.  Create a custom weather message.
5.  Predict the temperature
6.  Send a pushover message with the weather data

**For manual testing or running outside of the scheduled time:**

1. Open terminal in visual studio code or IDE
2. Go to folder containing main.py file
3. Type in "python main.py"
4. Press enter to run it
