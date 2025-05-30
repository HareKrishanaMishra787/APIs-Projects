import requests
from datetime import datetime
import os

# Your personal data. Used by Nutritionix to calculate calories.
GENDER = "male"
WEIGHT_KG = 65
HEIGHT_CM = 175
AGE = 24

# Nutritionix APP ID and API Key. Actual values are stored as environment variables.
APP_ID = os.environ["ENV_NIX_APP_ID"]
API_KEY = os.environ["ENV_NIX_API_KEY"]

exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"


exercise_text = input("Tell me which exercises you did: ")

# Nutritionix API Call
headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
}

parameters = {
    "query": exercise_text,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(exercise_endpoint, json=parameters, headers=headers)
result = response.json()
print(f"Nutritionix API call: \n {result} \n")


# Adding date and time
today_date = datetime.now().strftime("%d/%m/%Y")
now_time = datetime.now().strftime("%X")

# Sheety Project API. Check your Google sheet name and Sheety endpoint
GOOGLE_SHEET_NAME = "workout"
sheet_endpoint = os.environ["ENV_SHEETY_ENDPOINT"] #generated by sheety

# Sheety API Call & Authentication
# this is for our data in each row of every coloum sequently
for exercise in result["exercises"]:
    sheet_inputs = {
        GOOGLE_SHEET_NAME: {
            "date": today_date,
            "time": now_time,
            "exercise": exercise["name"].title(),
            "duration": exercise["duration_min"],
            "calories": exercise["nf_calories"]
        }
    }

    # Sheety Authentication Option 1: No Auth
    """
    sheet_response = requests.post(sheet_endpoint, json=sheet_inputs)
    """

    # Sheety Authentication Option 2: Basic Auth(this is for no one can access our google sheet without Authotication
    sheet_response = requests.post(
        sheet_endpoint,
        json=sheet_inputs,
        auth=(
            os.environ["ENV_SHEETY_USERNAME"],   # this is username
            os.environ["ENV_SHEETY_PASSWORD"],  #this is password
        )
    )


    print(f"Sheety Response: \n {sheet_response.text}")


    """ this is google spredsheet link "https://docs.google.com/spreadsheets/d/1jP7a5TajdFtkBtbwpivl4rFrbBY_Wxggi6ypKeJZeLA/edit?gid=0#gid=0" """
