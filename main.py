import os
import requests
import datetime as dt

GENDER = "female"
WEIGHT_KG = 45.5
HEIGHT_CM = 149
AGE = 24

APP_ID = os.environ.get("APP_ID")
API_KEY = os.environ.get("API_KEY")
NATURAL_EXERCISE = "https://trackapi.nutritionix.com/v2/natural/exercise"
POST_ROW = "https://api.sheety.co/d30c3372b580a6da32f7e544a74f3bc6/myWorkouts/workouts"

exercises = input("Tell me which exercises you did? ")

headers = {
    "x-app-id": APP_ID,
    "x-app-key": API_KEY,
    "Content-Type": "application/json"
}

input_data = {
    "query": exercises,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

response = requests.post(url=NATURAL_EXERCISE, json=input_data, headers=headers).json()
retrieved_data = [[record["name"], record["nf_calories"], record["duration_min"]] for record in response['exercises']]
sheety_headers = headers = {"Authorization": f"Bearer {os.environ.get('TOKEN')}"}

for activity in retrieved_data:
    data = {
        "workout": {
            "date": dt.datetime.now().date().strftime("%d/%m/%Y"),
            "time": dt.datetime.now().time().strftime("%I:%M:%S"),
            "exercise": activity[0].title(),
            "duration": activity[2],
            "calories": activity[1]
        }
    }
    response = requests.post(url=POST_ROW, json=data, headers=sheety_headers)
    print(response.text)
