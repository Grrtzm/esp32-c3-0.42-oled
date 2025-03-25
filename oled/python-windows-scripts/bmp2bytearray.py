# This program converts all *.bmp files in the current directory to bytearrays.
# You can use these bytearrays to create images for the oled.
# make sure the image resolution matches that of the oled display (72 x 40)
# Tip: Keep them a bit smaller; a width of 70 works for sure.

from PIL import Image
import os

def bmp_to_bytearray(bmp_path):
    # Open the BMP file
    img = Image.open(bmp_path)

    # Convert the image to monochrome (1-bit pixels, black and white)
    img = img.convert('1')

    # Get the image dimensions
    width, height = img.size

    # Initialize the bytearray
    byte_array = bytearray()

    # Iterate over the pixels and convert to bytearray
    for y in range(height):
        for x in range(0, width, 8):
            byte = 0
            for bit in range(8):
                if x + bit < width:
                    pixel = img.getpixel((x + bit, y))
                    if pixel == 0:  # Black pixel
                        byte |= (1 << (7 - bit))
            byte_array.append(byte)

    return byte_array

def convert_bmp_series(directory):
    bytearrays = []
    for file_name in os.listdir(directory):
        if file_name.endswith('.bmp'):
            file_path = os.path.join(directory, file_name)
            byte_array = bmp_to_bytearray(file_path)
            bytearrays.append((file_name, byte_array))
    return bytearrays

# Example usage
directory = '.'
bytearrays = convert_bmp_series(directory)

# Print the bytearrays
for file_name, byte_array in bytearrays:
    print(f"Bytearray for file {file_name}:")
    print(byte_array)
