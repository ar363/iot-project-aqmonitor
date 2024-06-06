import time
import board
import Adafruit_DHT
import RPi.GPIO as GPIO
import random
import pusher
from dotenv import load_dotenv
import os

load_dotenv()

push = pusher.Pusher(
    app_id=os.getenv("PUSHER_APPID"),
    key=os.getenv("PUSHER_KEY"),
    secret=os.getenv("PUSHER_SECRET"),
    cluster=os.getenv("PUSHER_CLUSTER"),
    ssl=True,
)

gaspin = 21
GPIO.setup(gaspin, GPIO.IN)

sensor = Adafruit_DHT.DHT11
pin = 4

while True:
    try:
        humidity, temperature = Adafruit_DHT.read(sensor, pin)
        if humidity is None or temperature is None:
            continue

        print(humidity, temperature)
        toxicgasdetected = GPIO.input(gaspin) == 0
        print("Harmful gas?: " + str(toxicgasdetected) + "\n")

        push.trigger(
            "raspi-proj",
            "status",
            {
                "temp": temperature + (random.randint(0, 5) / 10),
                "hum": humidity + (random.randint(0, 5) / 10),
                "gas": toxicgasdetected,
            },
        )

        time.sleep(1)

    except Exception as error:
        print("pin not wokring")
        print(error)
