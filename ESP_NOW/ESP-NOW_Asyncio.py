# Gert den Neijsel, 2025. The Hague University of Applied Sciences (Haagse Hogeschool).
# This is a demo program for an ESP32 C3 with 0.42" oled display.
# Push the button to send / broadcast a message using the ESP-NOW protocol to all ESP's running the same code.
# On the receiving ESP's the blue led lights up for a second and the name of the sending ESP is shown.

# If you only want to send send_messages to one or more specific receivers, add their wifi interface MAC address to the peer list:
# peer = b'\xa0\x85\xe3N\xf5\\' # Read the explanation below:
# e.add_peer(peer)
# If you don't understand the words used here, ask you favorite AI tool to explain them to you in your native language (Dutch?):

import network
import aioespnow
import asyncio
import machine
from machine import Pin, I2C
from ssd1306oled042b import SSD1306
from time import sleep
import framebuf
import ubinascii

# Create I2C interface
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

# Create and initialize OLED display
oled = SSD1306(i2c)
oled.clear()
oled.flip()  # Flip the display so it's readable when the USB connector is on top
ESP_NOW_logo = bytearray(b'\xff\x0f\x0f\xe0\x180xc\x8c\xff\x1f\x8f\xe0\x1c0\xfcc\x8c\xc01\xccp\x1c1\xcec\x8c\xc00\xcc0\x1e3\x872\x98\xc00\x0c0\x1a3\x036\xd8\xff>\x0cp\x1b3\x036\xd8\xff\x1f\x8f\xe0\x193\x036\xd8\xc0\x03\xcf\xc0\x19\xb3\x036\xd8\xc0\x00\xcc\x07\x98\xb3\x034\xd8\xc00\xcc\x07\x98\xf3\x87\x14P\xc09\xcc\x00\x18q\xce\x1cp\xff\x1f\x8c\x00\x18p\xfc\x1cp\xff\x0f\x0c\x00\x180x\x1cp')

def format_mac_address_as_string(mac): # Function to format MAC address as string
    return ''.join('\\x{:02x}'.format(byte) for byte in mac)

mac = bytearray(machine.unique_id())
macstr = format_mac_address_as_string(mac)
send_message = "ESP" + ubinascii.hexlify(mac).decode().upper()[-6:] # Message to send
# send_message = "Gert" # You could also send your own name; comment (#) the line above and uncomment this one

print(f"My MAC address as bytearray: b\'{macstr}\'") # You need this address for the peer list
print(f"Shortened MAC address (or message to send): {send_message}")
mac = ubinascii.hexlify(mac, ':').decode().upper()
print(f"My full MAC address: {mac}")

def display_logo_and_mac_address():
    fb = framebuf.FrameBuffer(ESP_NOW_logo, 70, 13, framebuf.MONO_HLSB)  # Load the 24x32 image binary data into a FrameBuffer
    oled.blit(fb, 0, 0)  # Project or "copy" the loaded image FrameBuffer into the OLED display
    oled.text(send_message, 0, 33, 1)  # Display the formatted MAC address
    oled.show()

display_logo_and_mac_address()

# A WLAN interface must be active
network.WLAN(network.WLAN.IF_STA).active(True)

e = aioespnow.AIOESPNow()
e.active(True)

peer = b'\xFF\xFF\xFF\xFF\xFF\xFF' # By using this address you broadcast to all ESP_NOW receivers.
e.add_peer(peer) # Do this for every individual peer. Don't forget to remove the broadcast address.

button = Pin(9, Pin.IN, Pin.PULL_UP)
led = Pin(8, Pin.OUT)
led.on() # Turns led off

async def sender(e, peer):
    while True:
        if not button.value():
            await e.asend(peer, send_message.encode())
            print("Sent message:",send_message)
            while not button.value(): # Remain is this loop as long as button is pressed
                await asyncio.sleep(0.1)
        else:
            await asyncio.sleep(0.01)  # Necessary to reduce CPU usage

async def receiver(e):
    while True:
        try:
            _, receive_message = await e.arecv()
            led.off() # Turns led on
            print("Received message:", receive_message.decode())
            oled.text(receive_message.decode(), 0, 20, 1)
            oled.show()
            await asyncio.sleep(1) # Wait a second
            led.on() # Turns led off
            oled.clear()
            display_logo_and_mac_address()
        except Exception as ex:
            print("Receive error:", ex)
            await asyncio.sleep(0.1)

async def main(e, peer):
    asyncio.create_task(sender(e, peer))
    asyncio.create_task(receiver(e))
    while True:
        await asyncio.sleep(1)

asyncio.run(main(e, peer))
