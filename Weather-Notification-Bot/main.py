import requests
from twilio.rest import Client


Own_Endpoints = "https://api.openweathermap.org/data/2.5/forecast"
api_key =  "0bc858da6991cb8446e199439d97779d"
account_sid = "ACd3eedb73ea2bd3b24a07accf35861219"
auth_token = "aee299c82acfd8394bcea33862d3a336"


weather_paramas = {
    "lat": 25.317644,
    "lon": 82.973915,
    "appid": api_key,
    "cnt" : 4  #this is timestamp to check whether for 12 hours forcast

}
# this is our API website https://openweathermap.org/forecast5
response = requests.get(url = Own_Endpoints,params=weather_paramas)
response.raise_for_status()
whether_data = response.json()
# to find the id whether_data["list"][x]["weather"][0]["id"] :
will_rain = False
for hour_data in whether_data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    #for every whether we have different whether id and if our id < 700 ( in documentation) than we must bring umbrella
    if int(condition_code)<700:
        will_rain = True
if will_rain:
    client = Client(account_sid, auth_token)  # this is to create our client at point where we want to send ourself a  SMS
    message = client.messages.create(
        body="It's going to rain today.Remember to bring an ☔", # this is Message which we want to send
        from_="+17622271541", #senders telephone number which we got from twillio site
        to="+919696850013", # this is phone number which we use to sign up to twillio
    )
    print(message.status)  # this  is to verify that our message is sent succesfully
