import datetime as dt
import random
import smtplib
import pandas as pd

my_email = "your@email.com"
password = "your_app_password"

birthdays = pd.read_csv("birthdays.csv")
birthdays_dict = birthdays.to_dict()
print(birthdays_dict)

today = dt.datetime.now()
now_month = today.month
now_date = today.day

letter_templates = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]


for i in range(len(birthdays_dict["name"])):
    if now_month == birthdays_dict["month"][i] and now_date == birthdays_dict["day"][i]:
        random_letter = random.choice(letter_templates)
        with open(f"{random_letter}", "r") as letter:
            letter_data = letter.read()
            new = letter_data.replace("[NAME]", birthdays_dict["name"][i])

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs=f"{birthdays_dict["email"][i]}",
                                msg=f"Subject:Happy Birthday !\n\n {new}"
                                )