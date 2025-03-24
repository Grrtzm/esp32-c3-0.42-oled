from machine import Pin
from time import sleep

# Definieer de onboard LED pin (meestal GPIO2)
led = Pin(8, Pin.OUT)

while True:
    led.value(1)  # Zet de LED aan
    sleep(0.5)    # Wacht 0.5 seconden
    led.value(0)  # Zet de LED uit
    sleep(0.5)    # Wacht 0.5 seconden
