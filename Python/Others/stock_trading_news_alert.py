import smtplib
import requests
import datetime
import os

MY_EMAIL = os.getenv("MY_EMAIL")
MY_PASSWORD = os.getenv("MY_PASSWORD")
STOCK = "RELIANCE.BSE"
COMPANY_NAME = "Reliance"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
stock_api_key = os.getenv("STOCK_API_KEY")
news_api_key = os.getenv("NEWS_API_KEY")

today_date = datetime.datetime.now().date()
yesterday_date = today_date - datetime.timedelta(days=1)
day_before_yesterday = today_date - datetime.timedelta(days=2)

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": stock_api_key,
}

try:
    stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
    stock_response.raise_for_status()
    stock_data = stock_response.json()

    close_price_yesterday = float(stock_data["Time Series (Daily)"][str(yesterday_date)]["4. close"])
    close_price_day_before_yesterday = float(stock_data["Time Series (Daily)"][str(day_before_yesterday)]["4. close"])

    price_difference = close_price_yesterday - close_price_day_before_yesterday
    price_difference_percent = (abs(price_difference) / close_price_day_before_yesterday) * 100

    if price_difference_percent >= 5:
        news_parameters = {
            "q": COMPANY_NAME,
            "sortBy": "publishedAt",
            "pageSize": 3,
            "apiKey": news_api_key,
        }
        news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
        news_response.raise_for_status()
        news_data = news_response.json()
        articles = news_data["articles"][:3]

        emoji = "🔺" if price_difference > 0 else "🔻"
        message = f"""Subject:{STOCK}: {emoji}{price_difference_percent:.2f}%\n\n"""

        for article in articles:
            message += f"""Headline: {article["title"]}\n\nRead more: {article["url"]}\n\n"""

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=message,
            )
except Exception as e:
    print(f"An error occurred: {e}")
