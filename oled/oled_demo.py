from machine import Pin, I2C
from ssd1306oled042b import SSD1306
import time
import framebuf
import math

# create I2C interface
i2c = I2C(0, sda=Pin(5), scl=Pin(6), freq=400000)

oled = SSD1306(i2c)
oled.flip()

# Function to draw a sinewave on the oled screen
def draw_sine_wave(oled):
    width = 72
    height = 40
    amplitude = height // 2
    offset = height // 2
    oled.vline(0,0,40,1)
    time.sleep(0.1)
    oled.hline(0,20,72,1)

    for x in range(width):
        y = int(amplitude * math.sin(2 * math.pi * x / width) + offset)
        oled.pixel(x, y, 1)
        oled.show()
        time.sleep(0.05)

while True:
    oled.clear()
    oled.invert(0)
    oled.text("123456789", 0, 0)
    oled.text("123456789", 0, 11)
    oled.text("123456789", 0, 22)
    oled.text("123456789", 0, 33)
    oled.show()
    time.sleep(1)

    # oled.line(0,0,71,0,1)   # top
    # oled.line(0,39,71,39,1) # bottom
    # oled.line(0,0,0,39,1)   # left
    # oled.line(71,0,71,39,1) # right

    # oled.fill_rect(0,0,71,39,1)  # same as the above

#     oled.clear()
    oled.rect(0,0,71,39,1)
    oled.show()
    time.sleep(1)

    # Load smiley face image and display
    # The below bytearray is a buffer representation of a 32x32 smiley face image. This is explained in this documentation below - continue reading!
#     smiley = bytearray(b'\x00?\xfc\x00\x00\xff\xff\x00\x03\xff\xff\xc0\x07\xe0\x07\xe0\x0f\x80\x01\xf0\x1f\x00\x00\xf8>\x00\x00|<\x00\x00<x\x00\x00\x1epx\x1e\x0e\xf0x\x1e\x0f\xe0x\x1e\x07\xe0x\x1e\x07\xe0\x00\x00\x07\xe0\x00\x00\x07\xe0\x00\x00\x07\xe1\xc0\x03\x87\xe1\xc0\x03\x87\xe1\xc0\x03\x87\xe1\xe0\x07\x87\xe0\xf0\x0f\x07\xf0\xf8\x1f\x0fp\x7f\xfe\x0ex?\xfc\x1e<\x0f\xf0<>\x00\x00|\x1f\x00\x00\xf8\x0f\x80\x01\xf0\x07\xe0\x07\xe0\x03\xff\xff\xc0\x00\xff\xff\x00\x00?\xfc\x00')
#     fb = framebuf.FrameBuffer(smiley, 32, 32, framebuf.MONO_HLSB) # load the 32x32 image binary data in to a FrameBuffer
#     bluetooth_icon = bytearray(b'\xff\x01\xff\xfc\x80\x7f\xf8\x00\x1f\xf0\x10\x0f\xe0\x18\x07\xc0\x1c\x03\xc0\x1e\x03\xc0\x1f\x03\x80\x1f\x81\x82\x19\xc1\x87\x19\xe1\x03\xd9\xc0\x01\xdf\x80\x00\xff\x00\x00~\x00\x00<\x00\x00<\x00\x00~\x00\x00\xff\x80\x01\xdb\x80\x83\x99\xc1\x07\x19\xe1\x82\x1d\xc1\xc0\x1f\x81\x80\x1e\x03\xc0\x1e\x03\xe0\x1c\x07\xe0\x18\x07\xf0\x10\x0f\xf8\x00\x1f\xfe\x00\x7f\xff\x83\xff')
    bluetooth_icon = bytearray(b'\x00\xfe\x00\x03\x7f\x80\x07\xff\xe0\x0f\xef\xf0\x1f\xe7\xf8?\xe3\xfc?\xe1\xfc?\xe0\xfc\x7f\xe0~}\xe6>x\xe6\x1e\xfc&?\xfe \x7f\xff\x00\xff\xff\x81\xff\xff\xc3\xff\xff\xc3\xff\xff\x81\xff\xff\x00\x7f\xfe$\x7f|f>\xf8\xe6\x1e}\xe2>?\xe0~\x7f\xe1\xfc?\xe1\xfc\x1f\xe3\xf8\x1f\xe7\xf8\x0f\xef\xf0\x07\xff\xe0\x01\xff\x80\x00|\x00')
    fb = framebuf.FrameBuffer(bluetooth_icon, 24, 32, framebuf.MONO_HLSB) # load the 24x32 image binary data in to a FrameBuffer

    oled.clear()
#     oled.blit(fb, 20, 4) # project or "copy" the loaded smiley image FrameBuffer into the OLED display
    oled.blit(fb, 24, 0) # project or "copy" the loaded smiley image FrameBuffer into the OLED display
    for n in range (4):
        oled.invert(0)
        oled.show()
        time.sleep(0.5)
        oled.invert(1)
        oled.show()
        time.sleep(0.5)

    for n in range (20):
        oled.scroll(3,2)
        oled.show()
        time.sleep(0.1)

    # Draw a sinewave
    oled.clear()
    oled.invert(0)
    draw_sine_wave(oled)
    time.sleep(1)

