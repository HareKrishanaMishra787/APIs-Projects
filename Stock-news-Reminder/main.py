import requests
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY= "LRAX8RG4U17UFJR1"
NEWS_API_KEY= "0e4adaddc09f431d90f66bacece0d4f9"
TWILIO_SID = "ACd3eedb73ea2bd3b24a07accf35861219"
TWILIO_AUTH_TOKEN = "aee299c82acfd8394bcea33862d3a336"


parameter = {
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY,
}


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
response = requests.get(STOCK_ENDPOINT,params=parameter)
data = response.json()["Time Series (Daily)"]
data_list = [value for (key,value) in data.items()]
yesterday_data = data_list[0]
yesterday_closing_price = float(yesterday_data["4. close"])
print(yesterday_closing_price)

#TODO 2. - Get the day before yesterday's closing stock price
day_before_yesterday = data_list[1]
day_before_yesterday_closing_price =float (day_before_yesterday["4. close"])
print(day_before_yesterday_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
difference =yesterday_closing_price-day_before_yesterday_closing_price
up_down = None
if difference>0:
    up_down= "🔺"
else:
    up_down="🔻"


#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percentage_difference = round((difference / yesterday_closing_price) * 100,2)
print(percentage_difference)




    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
""" check if difference is greater than 2 than we we got a notification """
if abs(percentage_difference)>2:
    new_params = {
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME

    }

    new_response= requests.get(NEWS_ENDPOINT,params=new_params)
    article = new_response.json()["articles"]

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
    three_articles = article[:3]
    print(three_articles)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    formatted_article_list = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \n {article['description']}" for article in three_articles]
    client = Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
#TODO 9. - Send each article as a separate message via Twilio.
    for article in formatted_article_list:
        message = client.messages.create(
            body=article,
            from_="+17622271541",
            to="+919696850013"
        )


    #Optional TODO: Format the message like this:
"""
we got notificatin like:
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""


