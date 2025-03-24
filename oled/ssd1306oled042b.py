import time
import framebuf
from machine import I2C, Pin

# Library created by combining and editing SH1106 and SSD1306 existing micropython libraries.
# Gert den Neijsel, The Hague University of Applied Sciences (with the help of ChatGPT)

class SSD1306:
    """
    A class to interface with the SSD1306 OLED display using I2C communication.
    Specifically adjusted the for the 72 x 40 pixel 0.42" display on the ESP32 C3 board by applying the correct x and y offsets (see below).
    """

    def __init__(self, i2c, address=0x3C):
        """
        Initializes the SSD1306 display.
      
        Parameters:
        i2c (I2C): The I2C bus object.
        address (int): The I2C address of the display (default: 0x3C).
        """
        self.i2c = i2c
        self.address = address
        self.width = 128   # buffer width
        self.height = 64   # buffer height
        self.offset_x = 28 # x offset for 0.42" display
        self.offset_y = 24 # y offset for 0.42" display
        self.flipped = False
        self.buffer = bytearray(self.width * self.height // 8)
        self.fb = framebuf.FrameBuffer(self.buffer, self.width, self.height, framebuf.MONO_VLSB)
        self.init_display()

    def init_display(self):
        """
        Sends initialization commands to set up the display.
        """
        self.write_cmd(0xAE)  # Display off
        self.write_cmd(0xD5)  # Set display clock divide ratio
        self.write_cmd(0x80)
        self.write_cmd(0xA8)  # Set multiplex ratio
        self.write_cmd(0x3F)
        self.write_cmd(0xD3)  # Set display offset
        self.write_cmd(0x00)
        self.write_cmd(0x40 | 0x00)  # Set start line to 0
        self.write_cmd(0x8D)  # Enable charge pump
        self.write_cmd(0x14)  # Brightness level. Default: 0x14, maximum: 0x1E
        self.write_cmd(0x20)  # Set memory addressing mode to horizontal
        self.write_cmd(0x00)
        self.write_cmd(0xA1)  # Set segment re-map (flip horizontally)
        self.write_cmd(0xC8)  # Set COM output scan direction (flip vertically)
        self.write_cmd(0xDA)  # Set COM pins
        self.write_cmd(0x12)
        self.write_cmd(0x81)  # Set contrast
        self.write_cmd(0xCF)  # Default: 0xCF
        self.write_cmd(0xD9)  # Set pre-charge period
        self.write_cmd(0xF1)  # Default: 0xF1
        self.write_cmd(0xDB)  # Set VCOMH deselect level
        self.write_cmd(0x40)
        self.write_cmd(0xA4)  # Disable entire display on
        self.write_cmd(0xA6)  # Set normal display
        self.write_cmd(0xAF)  # Display on
        self.clear()
        self.show()
    
    def write_cmd(self, cmd):
        """
        Sends a command byte to the display.
        
        Parameters:
        cmd (int): The command byte to send.
        """
        self.i2c.writeto(self.address, bytearray([0x00, cmd]))
    
    def show(self):
        """
        Updates the display with the contents of the framebuffer.
        """
        for page in range(8):
            self.write_cmd(0xB0 + page)
            self.write_cmd(0x00 + self.offset_x % 16)
            self.write_cmd(0x10 + self.offset_x // 16)
            self.i2c.writeto(self.address, bytearray([0x40]) + self.buffer[page * self.width:(page + 1) * self.width])
    
    def clear(self):
        """
        Clears the display by filling the framebuffer with zeros.
        """
        self.fb.fill(0)
    
    def apply_offset(self, x, y):
        """
        Applies the current display offset to the given coordinates.
        """
        if self.flipped:
            return x, y
        else:
            return x, y + self.offset_y
    
    def pixel(self, x, y, color):
        """
        Draws a pixel at the specified coordinates.
        
        Parameters:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        color (int): Pixel color (1 for white, 0 for black).
        """
        x, y = self.apply_offset(x, y)
        self.fb.pixel(x, y, color)
    
    def text(self, string, x, y, color=1):
        """
        Draws text at the specified coordinates.
        
        Parameters:
        x (int): X-coordinate.
        y (int): Y-coordinate.
        color (int): Pixel color (1 for white, 0 for black).
        """
        x, y = self.apply_offset(x, y)
        self.fb.text(string, x, y, color)
    
    def flip(self):
        """
        Flips the display 180 degrees.
        """
        self.flipped = not self.flipped
        if self.flipped:
            self.write_cmd(0xA0)
            self.write_cmd(0xC0)
    
    def invert(self, invert):
        """
        Inverts the display colors.
        
        Parameters:
        invert (bool): True to invert colors, False for normal mode.
        """
        self.write_cmd(0xA7 if invert else 0xA6)
    
    def power(self, on):
        """
        Turns the display on or off.
        
        Parameters:
        on (bool): True to turn on, False to turn off.
        """
        self.write_cmd(0xAF if on else 0xAE)

    def contrast(self, level):
        """
        Sets the display contrast.
        
        Parameters:
        level (int): Contrast level (0-255).
        """
        self.write_cmd(0x81)
        self.write_cmd(level)
    
    def line(self, x1, y1, x2, y2, color):
        """
        Draws a line between two points.
        """
        x1, y1 = self.apply_offset(x1, y1)
        x2, y2 = self.apply_offset(x2, y2)
        self.fb.line(x1, y1, x2, y2, color)
    
    def hline(self, x, y, w, color):
        """
        Draws a horizontal line with given width w.
        """
        x, y = self.apply_offset(x, y)
        self.fb.hline(x, y, w, color)
    
    def vline(self, x, y, h, color):
        """
        Draws a vertical line with given width w.
        """
        x, y = self.apply_offset(x, y)
        self.fb.vline(x, y, h, color)
    
    def fill(self, color):
        """
        Fills the entire display with a given color.
        color (int): Pixel color (1 for white, 0 for black).
        """
        self.fb.fill(color)
    
    def fill_rect(self, x, y, w, h, color):
        """
        Draws a filled rectangle.
        """
        x, y = self.apply_offset(x, y)
        self.fb.fill_rect(x, y, w, h, color)
    
    def rect(self, x, y, w, h, color):
        """
        Draws a rectangle outline.
        """
        x, y = self.apply_offset(x, y)
        self.fb.rect(x, y, w, h, color)
    
    def scroll(self, dx, dy):
        """
        Scrolls the display content.
        """
        self.fb.scroll(dx, dy)
    
    def blit(self, fb, x, y):
        """
        Copies another framebuffer to this display.
        """
        x, y = self.apply_offset(x, y)
        self.fb.blit(fb, x, y)
