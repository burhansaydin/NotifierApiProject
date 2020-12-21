import requests
from datetime import datetime
import smtplib
import time


MY_LAT = 37.983810 # Your latitude
MY_LONG = 23.727539 # Your longitude
password = "qetuo123"
my_email = "qazxswqaz04@gmail.com"


response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.
def position_check():
    return (abs(MY_LAT-iss_latitude) <= 5) and (abs(MY_LONG-iss_longitude) <= 5)


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now()
hour = time_now.hour


while True:
    time.sleep(60)
    if position_check() and sunset <= hour:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs= my_email,
                msg="Subject:Look Up \n\n The ISS is above you in the sky."
            )



