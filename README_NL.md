# ESP32-C3-0.42-oled
[Klik hier voor de Engelse versie van deze uitleg](README.md)

![ESP32-C3 met 0.42" oled-display](/images/esp32-c3-0.42-oled-pinout.png)

Deze repository bevat MicroPython voorbeeldcode en een aangepaste SSD1306-bibliotheek voor dit module, bedoeld voor gebruik tijdens het eerste semester van een hbo-opleiding 'HBO-ICT' aan De Haagse Hogeschool.

Ik wil dat leren leuk is. Ik heb dit apparaat gekozen vanwege de vele mogelijkheden. Laag niveau activiteiten zoals het laten knipperen van leds of het uitlezen van de status van een schakelaar zijn noodzakelijk om embedded systemen te leren begrijpen, maar zijn niet erg spannend. Met deze module kun je draadloze activiteiten uitvoeren zoals communiceren via 'Bluetooth Low Energy' (BLE) en Wi-Fi, en dit combineren met een Android-app, website of communiceren met een pc (Python-programma).
Om de mogelijkheden verder uit te breiden, kun je het op een [breadboard](/images/ESP32-c3-oled-breadboard-hc-sr04p_bb.png) plaatsen en [sensoren](/images/ESP32-c3-oled-breadboard-imu_bb.png) en [actuatoren](/images/ESP32-c3-oled-breadboard-servo_bb.png) aansluiten.

Alle (Micro)Python code in deze repository, inclusief de oled library is met AI gegenereerd met aanpassen door mij.

## Hoe gebruik je deze repository?
Installeer eerst [Thonny](/manual/Install_Thonny_[nl].pdf). Dit heb je nodig om alle voorbeelden uit te proberen. Laat je inspireren en gebruik de meegeleverde AI-prompt.
Je wordt aangemoedigd om [Generatieve AI](/Generative_AI/readme.md) maximaal te gebruiken. Laat AI nieuwe code genereren op basis van de voorbeelden en de code (en software) aan je uitleggen.

## Aanbevolen software voor gebruik met deze repository:

 - Vereist: [Thonny](https://thonny.org/) voor het bewerken en uitvoeren van MicroPython-code op de ESP32-C3.
	- Gebruik deze [Thonny installatiehandleiding](/manual/Install_Thonny_[nl].pdf) om Thonny en de ESP32-C3 voor MicroPython te installeren en configureren.
 - Optioneel: [Anaconda](https://anaconda.org/) voor het uitvoeren van Python en mogelijk het gebruik van Bluetooth (als je pc dit ondersteunt) op een Windows-pc, vergelijkbaar met wat je met een smartphone-app kunt doen.
	- Ik leg niet uit hoe je dit installeert, maar zorg ervoor dat je een [omgeving aanmaakt](https://www.anaconda.com/docs/tools/working-with-conda/environments) voor je ESP32-projecten.
 - [MIT App Inventor](https://appinventor.mit.edu/) voor het maken van Android- of IOS-apps (in combinatie met BLE).

## De volgende bestanden en mappen maken deel uit van deze repository:

In de **basics** map:

 - `blink.py`;
	 - de "Hello World" van embedded apparaten. Probeer dit eerst om je setup te controleren.
 - `toggle_without_delay.py`;
	 - gebruik de BOOT-knop om de led te schakelen en bekijk een niet-blokkerend alternatief voor delay.

Bekijk ook de **oled** map:

- `oled_demo.py`
- `oled_running_men.py`

(Vergeet niet de oled-driver naar de ESP32 te kopiëren.)

Als je van 'running men' houdt, hier is de tool die ik gebruikte om het te maken: `/oled/python-windows-scripts/bmp2bytearray.py`

## Draadloze communicatie

In de **BLE** map:
- `BLE_Led_on_off.py` te gebruiken met [`ESP32C3_Led_Control.apk`](/app-related/ESP32C3_Led_Control.apk)
	- Demonstreert het gebruik van een app die alleen **data schrijft** naar de ESP32 via BLE.
- `BLE_Read_Button.py` te gebruiken met [`ESP32C3_Read_Button.apk`](/app-related/ESP32C3_Read_Button.apk)
	- Demonstreert het gebruik van een app die alleen **data leest** van de ESP32 via BLE.
- `BLE_Read_Write_Led_PWM.py` te gebruiken met [`ESP32C3_RW_Led_PWM.apk`](/app-related/ESP32C3_RW_Led_PWM.apk)
	- Demonstreert het gebruik van een app die **data leest en schrijft** van en naar de ESP32 via BLE.

Wil je je eigen MIT App Inventor-app maken? Bekijk dan de map /app-related.

In de **IP** map:
- `AP_webserver.py`: Wi-Fi access point en webserver tegelijk.
- `WiFi_Client_webserver.py`: Verbind de ESP eerst met Wi-Fi.

In de **ESP_NOW** map:

- `ESP_NOW`: Broadcast naar meerdere apparaten en ontvang tegelijkertijd.

## Voor Debugging #

- `/i2c/i2c_scanner.py`: helpt je i2c-sensoren en apparaten te vinden die correct op de ESP32 zijn aangesloten.

