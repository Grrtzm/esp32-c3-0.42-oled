# Gert den Neijsel, 2025. The Hague University of Applied Sciences (Haagse Hogeschool).
# This is a demo program for an ESP32 C3 with 0.42" oled display.
# The ESP32-C3 will set up it's own Wi-Fi network, "ESP-C3".
# Connect you PC to this Wi-Fi network, you do not need a password.
# Copy the IP address and paste it in your browser.
# Now you have a webpage with ON and OFF buttons. They will switch the LED on the ESP32-C3 ON or OFF.

# Please note: Some of the ESP32-C3 boards have a poor quality Wi-Fi antenna (the red block),
# which makes connecting to Wi-Fi hard or sometimes impossible.
# Touching the antenna might help. Pressing the reset button might help.

import network
import socket
from machine import Pin

# Setup the Wi-Fi Access Point
ap = network.WLAN(network.AP_IF)
ap.config(essid="ESP-C3", password="")  # Open network
# ap.config(essid="ESP-C3", password="YourPassword", authmode=3) # authmode=3 = WPA2-PSK (recommended)

ap.active(True)
while not ap.active():
    pass
print("Access Point active! IP-address:", ap.ifconfig()[0])

# Setup Onboard LED (GPIO8 on ESP32-C3 boards)
led = Pin(8, Pin.OUT)
led.value(0)  # LED off at startup

def web_page():
    return """<!DOCTYPE html>
    <html>
    <head>
        <title>ESP32-C3 Webserver</title>
        <style>
            body { text-align: center; font-family: Arial; }
            .button { display: inline-block; padding: 20px; font-size: 20px; width: 100px; }
            .on { background-color: green; color: white; }
            .off { background-color: red; color: white; }
        </style>
    </head>
    <body>
        <h1>ESP32-C3 LED Control</h1>
        <a href="/on"><button class="button on">ON</button></a>
        <a href="/off"><button class="button off">OFF</button></a>
    </body>
    </html>"""

# Setup Webserver
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    
    if "GET /on" in request:
        led.value(0)  # LED ON
    elif "GET /off" in request:
        led.value(1)  # LED OFF
    
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n" + response)
    conn.close()
