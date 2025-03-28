# Gert den Neijsel, 2025. The Hague University of Applied Sciences (Haagse Hogeschool).
# This is a demo program for an ESP32 C3 with 0.42" oled display.
# Let the ESP32-C3 join a Wi-Fi network.
# Copy the IP address and paste it in your browser.
# Now you have a webpage with ON and OFF buttons. They will switch the LED on the ESP32-C3 ON or OFF.

# Please note: The ESP32-C3 oled boards have a poor quality Wi-Fi antenna (the red block),
# which makes connecting to Wi-Fi hard or sometimes impossible.
# Lightly touching/holding the antenna all the time might help.
# Better yet: solder an antenna wire of 31mm length to the "reset button" side of the red block.
# Because of this, the code contains a lot of signal- and connection state debugging code.

# Note: if you interrupt the code with Ctrl+C or when you restart the code, Wi-Fi is blocked.
# Press reset and click "STOP"/Restart to be able to start the program again.

import network
import socket
import time
from machine import Pin, I2C
import uasyncio as asyncio
from ssd1306oled042b import SSD1306
import framebuf

# Maak I2C interface aan
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

# Initialize OLED display (if it exists)
oled_found = True # Assume it exists
try:
    oled = SSD1306(i2c)
except OSError as e:
    if e.errno == 19:  # ENODEV: No such device
        print("Error: OLED-display not Found. Check the I2C-connections.")
    else:
        print(f"OLED-error: {e}")
    oled_found = False  # Oled doesn't exist. Use this to prevent further errors

def display_logo():
    fb = framebuf.FrameBuffer(WiFi_logo, 52, 40, framebuf.MONO_HLSB)  # Load the 24x32 image binary data into a FrameBuffer
    oled.blit(fb, 9, 0)  # Project or "copy" the loaded image FrameBuffer into the OLED display
    # oled.invert(True)
    oled.show()

if oled_found:
    oled.clear()
    oled.flip()  # Flip the display so it's readable when the USB connector is on top
    WiFi_logo = bytearray(b'\xff\xff\xff\xff\xff\xff\xf0\xff\xff\xf0\x00\xff\xff\xf0\xff\xff\xc0\x00?\xff\xf0\xff\xff\x00\x00\x0f\xff\xf0\xff\xfc\x00\x00\x03\xff\xf0\xff\xf8\x00\x00\x01\xff\xf0\xff\xf0\x00\x00\x00\xff\xf0\xf8\x00\x00\x00\x00\x01\xf0\xe0\x00\x00\x00\x00\x00p\xc0\x00\x00\x00\x00\x000\x80\x00\x00\x00\x7f\xf8\x10\x80\x00\x00\x01\xff\xfe\x10\x00\x00\x00\x03\xff\xff\x00\x00\x00\x00\x03\xff\xff\x00\x1e8\xe1\xc7\x01\xc7\x80\x0e8\xe1\xc7\x01\xc7\x80\x0e8\xe1\xc7\x01\xc7\x80\x0ey\xe0\x07\x1f\xff\x80\x0e}\xc0\x07\x1f\xff\x80\x07}\xc0\x07\x1f\xff\x80\x07m\xc1\xc7\x01\xc7\x80\x07\xed\xc1\xc7\x01\xc7\x80\x07\xef\x81\xc7\x01\xc7\x80\x03\xcf\x81\xc7\x1f\xc7\x80\x03\xcf\x81\xc7\x1f\xc7\x80\x03\xc7\x81\xc7\x1f\xc7\x80\x01\xc7\x01\xc7\x1f\xc7\x00\x00\x00\x00\x07\xff\xff\x00\x80\x00\x00\x0f\xff\xfe\x10\x80\x00\x00?\xff\xf8\x10\xc0\x00\x00\x00\x00\x000\xe0\x00\x00\x00\x00\x00p\xf8\x00\x00\x00\x00\x01\xf0\xff\xf0\x00\x00\x00\xff\xf0\xff\xf8\x00\x00\x01\xff\xf0\xff\xfc\x00\x00\x03\xff\xf0\xff\xff\x00\x00\x0f\xff\xf0\xff\xff\x80\x00\x1f\xff\xf0\xff\xff\xf0\x00\xff\xff\xf0\xff\xff\xff\x9f\xff\xff\xf0')
    oled.show()
    display_logo()

# Onboard LED (inverted logic: LOW = ON, HIGH = OFF)
led = Pin(8, Pin.OUT)
led.value(1)  # LED off at startup

# Standard WiFi-settings (use these if you always want to connect automatically)
SSID = "YourSSID"  # <-- Enter your network name
PASSWORD = "YourPassword"  # <-- Enter your password
USE_PREDEFINED_WIFI = False  # Set to True to automatically connect using the settings above

# WiFi-initialisation
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def print_wifi_status():
    status_codes = {
        1000: "STAT_IDLE - Wi-Fi is enabled but not connected.                         ",
        1001: "STAT_CONNECTING - Connecting to the network.                            ",
        1010: "STAT_GOT_IP - Connected and IP address assigned.                        ",
        1002: "STAT_WRONG_PASSWORD - Incorrect password.                               ",
        1003: "STAT_NO_AP_FOUND - SSID not found (out of range or incorrect).          ",
        1004: "STAT_CONNECT_FAIL - Connection failed for another reason.               ",
        202:  "STAT_BEACON_TIMEOUT - No Wi-Fi beacons received, possible signal issue. "
    }
    status = wlan.status()
    meaning = status_codes.get(status, f"UNKNOWN STATUS CODE: {status}")
    print(f"\rWi-Fi Status: {status} -> {meaning}", end="") # Print without linefeed and new line

def explain_signal_strength():
    print("\nPlease note: Signal strength (dBm) is measured in decibel-milliwatts (dBm).")
    print("The closer to 0, the stronger the signal. For example:")
    print("-30 dBm: Excellent signal.")
    print("-65 dBm: Lowest value at which an ESP32-C3 could connect to Wi-Fi and maintain the connection.")
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
        channel = net[4]  # Wi-Fi channel
        print(f"{i}: {ssid:<30} Signal strength: {signal_strength} dBm, Channel: {channel}")
    explain_signal_strength()
    
    # Let the user choose a network
    ssid_index = int(input("Select a network (enter the number): "))
    SSID = networks[ssid_index][0].decode()  # Select SSID 
    PASSWORD = input(f"Password for {SSID}: ")

async def update_signal_strength():
    """Toont de Wi-Fi signaalsterkte elke seconde."""
    while True:
        signal_strength = wlan.status('rssi')
        print(f"Wi-Fi Signal Strength: {signal_strength} dBm     ", end="\r")  # Spaces to delete old text
        await asyncio.sleep(1)  # Wacht 1 seconde

async def handle_request(reader, writer):
    """Afhandelen van inkomende HTTP-verzoeken."""
    request = await reader.read(1024)
    request = request.decode()
    addr = writer.get_extra_info('peername')
    print(f"\nRequest from {addr}: {request}")

    # LED ON/OFF
    if "/?led=on" in request:
        led.value(0)  # ON (inverted logic)
    elif "/?led=off" in request:
        led.value(1)  # OFF

    # Send HTML response
    response = web_page()
    writer.write("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n".encode() + response.encode())
    await writer.drain()
    writer.close()
    await writer.wait_closed()

async def start_webserver():
    """Start an asynchronous webserver."""
    server = await asyncio.start_server(handle_request, "0.0.0.0", 80)
    print(f"Webserver running on IP: {ip}")

    while True:
        await asyncio.sleep(1)  # Keep the server running

# Connect to WiFi
print(f"Connecting to {SSID}...")
wlan.connect(SSID, PASSWORD)

# Wait for connection
timeout = 60  # 10 sec timeout
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1
    print_wifi_status()
    print(timeout, end="\r") # Print in the same spot all the time, no "\n" line feed 

# Check if the connection is succesfull
if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print(f"\nConnected!\nIP-address: {ip}")
else:
    print("Connected failed.")
    wlan.active(False)
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

async def main():
    await asyncio.gather(update_signal_strength(), start_webserver()) # Start two separate tasks (multitasking)

asyncio.run(main())