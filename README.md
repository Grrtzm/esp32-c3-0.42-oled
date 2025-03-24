# esp32-c3-0.42-oled
This repository contains MicroPython example code and customized SSD1306 library for this module for use during the first semester of a college level course 'HBO-ICT' at 'The Hague University of Applied Sciences'

I want learning to be fun and selected this module because of the all the things you can do with it. Low level things like blinking leds or reading the state of a switch are necessary but not very exciting. With this module you can do wireless things like communicating via 'Bluetooth Low Energy' (BLE) and Wi-Fi and combine it with an Android app, website, or communicate with it via a PC (Python) program.

![SparkFun Pro Micro ESP32-C3 (DEV-23484)](https://www.sparkfun.com/products/23484)
I recommend to use the following software with the code in this repository:

 - Thonny for editing and running the MicroPython code on the ESP32c3.
 - Anaconda for running Python on a (Windows) PC
 - MIT App Inventor for creating Android apps (combined with the use of BLE).

The following files and folders are part of this repository:
In the **basics** folder:
 - `blink.py`; 
	 - the "Hello World" of embedded devices
 - `toggle_without_delay.py`;
	 - use the BOOT button to toggle the led and shows a non-blocking alternative for delay 

In the **BLE** folder:
- `BLE_Led_on_off.py` to be used with `ESP32C3_Led_Control.apk`
	- Demonstrates the use of an app which only **writes** data to the ESP32 via BLE
- `BLE_Read_Button.py` to be used with `ESP32C3_Read_Button.apk`
	- Demonstrates the use of an app which only **reads** data from the ESP32 via BLE
- `BLE_Read_Write_Led_PWM.py` to be used with `ESP32C3_RW_Led_PWM.apk`
	- Demonstrates the use of an app which **reads and writes** data to and from the ESP32 via BLE

BLE\py-win-scripts
BLE\ssd1306oled042b.py
BLE\py-win-scripts\BLE_Read_BOOT_button.py
BLE\py-win-scripts\BLE_Read_Write_Led_PWM.py
BLE\py-win-scripts\bluetoothUART.py
BLE\py-win-scripts\img_convert.py
i2c\i2c_scanner.py
images\back.avif
images\ESP32-C3-pinout.png
IP\AP_webserver.py
IP\WiFi_Client_webserver.py
oled\oled_demo.py
oled\ssd1306oled042b.py
