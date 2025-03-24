import network
import socket
import time
from machine import Pin

# Onboard LED (inverted logic: LOW = ON, HIGH = OFF)
led = Pin(8, Pin.OUT)
led.value(1)  # LED uit bij opstarten

# Standaard WiFi-instellingen (gebruik deze als je altijd automatisch wilt verbinden)
SSID = "JouwSSID"  # <-- Vul hier je netwerknaam in
PASSWORD = "JouwWachtwoord"  # <-- Vul hier je wachtwoord in
USE_PREDEFINED_WIFI = False  # Zet op True om automatisch te verbinden


# WiFi-initialisatie
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

if not USE_PREDEFINED_WIFI:
    # WiFi-netwerken scannen
    print("Scannen naar beschikbare netwerken...")
    networks = wlan.scan()
    available_ssids = [net[0].decode() for net in networks]

    # Lijst met SSID's weergeven
    print("Beschikbare netwerken:")
    for i, ssid in enumerate(available_ssids):
        print(f"{i}: {ssid}")

    # Gebruiker een SSID laten kiezen
    ssid_index = int(input("Kies een netwerk (nummer invoeren): "))
    SSID = available_ssids[ssid_index]
    PASSWORD = input(f"Wachtwoord voor {SSID}: ")

# Verbinden met WiFi
print(f"Verbinden met {SSID}...")
wlan.connect(SSID, PASSWORD)

# Wachten op verbinding
timeout = 10  # 10 sec timeout
while not wlan.isconnected() and timeout > 0:
    time.sleep(1)
    timeout -= 1

# Controleren of verbinding gelukt is
if wlan.isconnected():
    ip = wlan.ifconfig()[0]
    print(f"Verbonden!\nIP-adres: {ip}")
else:
    print("Verbinding mislukt. Herstart en probeer opnieuw.")
    raise SystemExit

# Webserver starten
def web_page():
    """Genereert de HTML voor de webpagina."""
    led_state = "AAN" if led.value() == 0 else "UIT"
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
        <a href="/?led=on"><button class="btn btn-on">AAN</button></a>
        <a href="/?led=off"><button class="btn btn-off">UIT</button></a>
    </body>
    </html>"""
    return html

# Webserver socket opzetten
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 80))
server_socket.listen(5)
print("Webserver draait op IP:", ip)

# HTTP-verzoeken verwerken
while True:
    conn, addr = server_socket.accept()
    request = conn.recv(1024).decode()
    print(f"Verzoek van {addr}: {request}")

    # LED aan/uit zetten
    if "/?led=on" in request:
        led.value(0)  # AAN (inverted logic)
    elif "/?led=off" in request:
        led.value(1)  # UIT

    # HTML-pagina terugsturen
    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\nConnection: close\n\n" + response)
    conn.close()
