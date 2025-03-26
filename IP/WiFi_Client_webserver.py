# Gert den Neijsel, 2025. The Hague University of Applied Sciences (Haagse Hogeschool).
# This is a demo program for an ESP32 C3 with 0.42" oled display.
# Let the ESP32-C3 join a Wi-Fi network.
# Copy the IP address and paste it in your browser.
# Now you have a webpage with ON and OFF buttons. They will switch the LED on the ESP32-C3 ON or OFF.

# Please note: Some of the ESP32-C3 boards have a poor quality Wi-Fi antenna (the red block),
# which makes connecting to Wi-Fi hard or sometimes impossible.
# Touching the antenna might help. Pressing the reset button might help.

import network
import socket
import time
from machine import Pin

# Onboard LED (inverted logic: LOW = ON, HIGH = OFF)
led = Pin(8, Pin.OUT)
led.value(1)  # LED off at startup

# Standard WiFi-settings (use these if you always want to connect automatically)
SSID = "YourSSID"  # <-- Enter your network name
PASSWORD = "YourPassword"  # <-- Vul hier je wachtwoord in
USE_PREDEFINED_WIFI = False  # Set to True to automatically connect using the settings above


# WiFi-initialisation
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def explain_signal_strength():
    print("\nPlease note: Signal strength (dBm) is measured in decibel-milliwatts (dBm).")
    print("The closer to 0, the stronger the signal. For example:")
    print("-30 dBm: Excellent signal.")
    print("-67 dBm: Suitable for streaming.")
    print("-90 dBm: Weak signal.")

if not USE_PREDEFINED_WIFI:
    # Scan for WiFi-netwerken
    print("Scanning for available networks...")
    networks = wlan.scan()

    # Display available networks
    print("Available networks:")
    for i, net in enumerate(networks):
        ssid = net[0].decode()  # The SSID for the network
        signal_strength = net[3]  # Signal strength in dBm
        print(f"{i}: {ssid:<30} Signal strength: {signal_strength} dBm")

    explain_signal_strength()
    
    # Let the user choose a network
    ssid_index = int(input("Select a network (enter the number): "))
    SSID = networks[ssid_index][0].decode()  # SSID selecteren
    PASSWORD = input(f"Password for {SSID}: ")

# Connect to WiFi
print(f"Connecting to {SSID}...")
wlan.connect(SSID, PASSWORD)

# Wait for connection
timeout = 10  # 10 sec timeout
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

# Check if the connection is succesfull
if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print(f"Connected!\nIP-address: {ip}")
else:
    print("Connected failed. Power off and on and try again.")
    raise SystemExit

# Start Webserver
def web_page():
    """Genererates the HTML for the webpagina."""
    led_state = "ON" if led.value() == 0 else "OFF"
    html = f"""<!DOCTYPE html>
    <html>
    <head>
    <title>ESP32 LED Control</title>
    <style>
        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
        .btn {{ display: inline-block; font-size: 20px; padding: 15px; margin: 10px; width: 100px; border: none; cursor: pointer; }}
        .btn-on {{ background-color: green; color: white; }}
        .btn-off {{ background-color: red; color: white; }}
    </style>
    </head>
    <body>
        <h2>ESP32_C3 onboard LED Control</h2>
        <p>LED Status: <strong>{led_state}</strong></p>
        <a href="/?led=on"><button class="btn btn-on">ON</button></a>
        <a href="/?led=off"><button class="btn btn-off">OFF</button></a>
    </body>
    </html>"""
    return html

# Setup Webserver socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen(5)
print("Webserver running on IP:", ip)

# Handle HTTP-requests
while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024).decode()
    print(f"Request from {addr}: {request}")

    # Switch LED on/off
    if "/?led=on" in request:
        led.value(0)  # ON (inverted logic)
    elif "/?led=off" in request:
        led.value(1)  # OFF

    # Send HTML response page
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n" + response)
    conn.close()
