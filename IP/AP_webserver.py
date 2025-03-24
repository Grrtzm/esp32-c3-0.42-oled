import network
import socket
from machine import Pin

# Wi-Fi Access Point instellen
ap = network.WLAN(network.AP_IF)
ap.config(essid="ESP-C3", password="")  # Open netwerk
# ap.config(essid="ESP-C3", password="JouwWachtwoord", authmode=3) # authmode=3 = WPA2-PSK (aanbevolen)

ap.active(True)
while not ap.active():
    pass
print("Access Point actief! IP-adres:", ap.ifconfig()[0])

# Onboard LED instellen (GPIO8 op veel ESP32-C3 boards)
led = Pin(8, Pin.OUT)
led.value(0)  # LED uit bij opstart

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
        <a href="/on"><button class="button on">Aan</button></a>
        <a href="/off"><button class="button off">Uit</button></a>
    </body>
    </html>"""

# Webserver instellen
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode()
    
    if "GET /on" in request:
        led.value(0)  # LED aan
    elif "GET /off" in request:
        led.value(1)  # LED uit
    
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n" + response)
    conn.close()
