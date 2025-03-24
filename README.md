# esp32-c3-0.42-oled
![ESP32-C3 with 0.42" oled display](/images/esp32-c3-0.42-oled-pinout.png)

This repository contains MicroPython example code and a customized SSD1306 library for this module for use during the first semester of a college level course 'HBO-ICT' at 'The Hague University of Applied Sciences'

I want learning to be fun. I selected this device because of the all the things you can do with it. Low level things like blinking leds or reading the state of a switch are necessary to learn about embedded systems but are not very exciting. With this module you can do wireless things like communicating via 'Bluetooth Low Energy' (BLE) and Wi-Fi and combine it with an Android app, website, or communicate with it via a PC (Python) program.
To further extend the possibilities with this device, you can put it on a [breadboard](/images/ESP32-c3-oled-breadboard-hc-sr04p_bb.png) and connect [sensors](/images/ESP32-c3-oled-breadboard-imu_bb.png) and [actuators](/images/ESP32-c3-oled-breadboard-servo_bb.png) to it.

You're encouraged to use [Generative AI](/Generative_AI/readme.md) To-The-Max. Let it generate new code from the examples and explain the code (and the software you use) to you.

I recommend using the following software with the code in this repository:

 - Required: [Thonny](https://thonny.org/) for editing and running the MicroPython code on the ESP32-C3.
	- Use this [Thonny setup guide](\basics\Install_Thonny_[en].pdf) to install and configure Thonny and the ESP32-C3 for MicroPython.
 - Optional: [Anaconda](https://anaconda.org/) for running Python and maybe use Bluetooth (if your PC supports this) on a (Windows) PC, a bit like what you can do with a smartphone app.
	- I'm not going to explain how to use or install this, but make sure you [create an environment](https://www.anaconda.com/docs/tools/working-with-conda/environments) where you work on your ESP32 related projects.
 - [MIT App Inventor](https://appinventor.mit.edu/) for creating Android or IOS apps (combined with the use of 'Bluetooth Low Energy' (BLE) ).

## The following files and folders are part of this repository:

In the **basics** folder:

 - `blink.py`; 
	 - the "Hello World" of embedded devices. Try this first to check your setup.
 - `toggle_without_delay.py`;
	 - use the BOOT button to toggle the led and shows a non-blocking alternative for delay 

Take a look in the **oled** folder:

- `oled_demo.py`
- `oled_running_men.py`

(Don't forget to copy the oled driver to the ESP32).

If you like 'running men'; here's the tool is used to create it: `\python-windows-scripts\bmp2bytearray.py`

## Wireless stuff

In the **BLE** folder:
- `BLE_Led_on_off.py` to be used with [`ESP32C3_Led_Control.apk`](/app-related/ESP32C3_Led_Control.apk)
	- Demonstrates the use of an app which only **writes** data to the ESP32 via BLE
- `BLE_Read_Button.py` to be used with [`ESP32C3_Read_Button.apk`](/app-related/ESP32C3_Read_Button.apk)
	- Demonstrates the use of an app which only **reads** data from the ESP32 via BLE
- `BLE_Read_Write_Led_PWM.py` to be used with [`ESP32C3_RW_Led_PWM.apk`](/app-related/ESP32C3_RW_Led_PWM.apk)
	- Demonstrates the use of an app which **reads and writes** data to and from the ESP32 via BLE

If you want to build your own MIT App Inventor app, take a look in the /app-related folder.

In the **IP** folder:
- `AP_webserver.py'`: 	Wi-Fi access point and webserver at the same time
- `WiFi_Client_webserver.py`: Connect the ESP to Wi-Fi first

In the **ESP_NOW** folder:

- `ESP_NOW`: broadcast to many devices and receive at the same time

## For Debugging #

- `/i2c/i2c_scanner.py`: helps you find i2c sensors and devices connected to the ESP32 (if you connected them correctly).

