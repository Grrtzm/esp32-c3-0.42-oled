# Gert den Neijsel, 2025. The Hague University of Applied Sciences (Haagse Hogeschool)
# This is a demo program for an ESP32 C3 with 0.42" oled display
# Combined with a custom app created with 'MIT App Inventor' you can read the
# status of the onboard BOOT button via Bluetooth Low Energy (BLE)
# This is a "Read Only" version;
# the (Android) app only receives commands from the ESP

import machine
from machine import Pin, I2C
from ssd1306oled042b import SSD1306
import bluetooth
from time import sleep
import framebuf
import ubinascii

# create I2C interface
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

# create oled display, print Bluetooth logo and MAC address
oled = SSD1306(i2c)

def display_logo_and_mac_address():
    mac = bytearray(machine.unique_id())  # Get the unique chip-ID (MAC address)
    mac[-1] = (mac[-1] + 2) % 256  # Add 2 to the last byte to match the advertising address
    print(ubinascii.hexlify(mac, ':').decode().upper())

    oled.clear()
    oled.flip() # Flip the display so it's readable when the USB connector is on top
    bluetooth_icon = bytearray(b'\x00\xfe\x00\x03\x7f\x80\x07\xff\xe0\x0f\xef\xf0\x1f\xe7\xf8?\xe3\xfc?\xe1\xfc?\xe0\xfc\x7f\xe0~}\xe6>x\xe6\x1e\xfc&?\xfe \x7f\xff\x00\xff\xff\x81\xff\xff\xc3\xff\xff\xc3\xff\xff\x81\xff\xff\x00\x7f\xfe$\x7f|f>\xf8\xe6\x1e}\xe2>?\xe0~\x7f\xe1\xfc?\xe1\xfc\x1f\xe3\xf8\x1f\xe7\xf8\x0f\xef\xf0\x07\xff\xe0\x01\xff\x80\x00|\x00')
    fb = framebuf.FrameBuffer(bluetooth_icon, 24, 32, framebuf.MONO_HLSB) # load the 24x32 image binary data in to a FrameBuffer
    oled.blit(fb, 24, 0) # project or "copy" the loaded smiley image FrameBuffer into the OLED display
    
    oled.text("But   ton",0,0,1) # Name for this project in the top left corner
    oled.text("ESP" + ubinascii.hexlify(mac).decode().upper()[-6:],0,33,1) # only use the 3 bytes on the right (6 chars), the left 3 bytes are the OUI (=ESP)
    oled.show()

display_logo_and_mac_address()

# Define the button
button = Pin(9, Pin.IN, Pin.PULL_UP)  # BOOT-knop op GPIO 9 (pull-up ingeschakeld)

# Maak een BLE-object
ble = bluetooth.BLE()
ble.active(True)

# Debug
print("BLE active:", ble.active())

# UUID's for the Nordic UART Service (NUS)
UART_SERVICE_UUID = bluetooth.UUID("6E400001-B5A3-F393-E0A9-E50E24DCCA9E")
UART_TX_CHAR_UUID = bluetooth.UUID("6E400002-B5A3-F393-E0A9-E50E24DCCA9E")
UART_RX_CHAR_UUID = bluetooth.UUID("6E400003-B5A3-F393-E0A9-E50E24DCCA9E")

# Create BLE service and characteristics
UART_SERVICE = (UART_SERVICE_UUID, [
    (UART_TX_CHAR_UUID, bluetooth.FLAG_READ | bluetooth.FLAG_NOTIFY),
    (UART_RX_CHAR_UUID, bluetooth.FLAG_WRITE)
])

# Register the BLE-service
handles = ble.gatts_register_services([UART_SERVICE])
tx_handle = handles[0][0]  # Handle voor TX characteristic
rx_handle = handles[0][1]  # Handle voor RX characteristic

# Start BLE advertising
def advertise():
    name = b"ESP32_UART"
    adv_data = b"\x02\x01\x06" + bytes([len(name) + 1, 0x09]) + name
    ble.gap_advertise(100, adv_data)
    print("Advertising gestart:", name.decode('utf-8'))

advertise()

# Variable to store the connection handle
conn_handle = None

# Variable to store the previous button state
prev_button_state = None

# Callback voor BLE events
def on_ble_event(event, data):
    global conn_handle
    if event == 1:  # CONNECT event
        conn_handle = data[0]
        print(f"Device connected, conn_handle: {conn_handle}")

    elif event == 2:  # DISCONNECT event
        print("Device disconnected, restarting advertising...")
        conn_handle = None
        advertise()

# Link the callback to BLE events
ble.irq(on_ble_event)

# main loop: read button state and notify via BLE if it changes
while True:
    if conn_handle is not None:
        button_state = not button.value()  # Active low, so invert the value
        if button_state != prev_button_state:
            oled.invert(button_state)
            try:
                ble.gatts_notify(conn_handle, tx_handle, str(button_state).encode('utf-8'))
                print(f"Button state changed: {button_state}")
                prev_button_state = button_state
            except OSError as e:
                print(f"Error sending notification: {e}")
        else:
            # Send regular updates even if the state hasn't changed
            try:
                ble.gatts_notify(conn_handle, tx_handle, str(button_state).encode('utf-8'))
            except OSError as e:
                print(f"Error sending regular update: {e}")
    sleep(0.1)