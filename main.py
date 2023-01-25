import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 0.264840
MY_LONG = 32.566799

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])

#Your position is within +5 or -5 degrees of the ISS position.


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

#If the ISS is close to my current position
def pos():
    if ((iss_latitude >= -5.264840) and (iss_latitude <= 5.264)) and\
            ((iss_longitude >= 27.566799) and (iss_longitude <= 37.566799)):
        # and it is currently dark
        if (hour < sunrise) and (hour > sunset):
            # Then send me an email to tell me to look up.
            with smtplib.SMTP("smtp.gmail.com", 587) as connection:
                connection.starttls()
                connection.login(user="leumaselulakk@gmail.com", password="my_password")
                connection.sendmail(
                    from_addr="leumaselulakk@gmail.com",
                    to_addrs="samuelkibirigek@gmail.com",
                    msg="Subject:ISS is overhead\n\nLook up to see the International Space Station. "
                )

#make the code run every 60s
while True:
    time.sleep(60)
    pos()




