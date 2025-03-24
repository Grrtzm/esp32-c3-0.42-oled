from machine import I2C, Pin

# Initialiseer I2C (gebruik de juiste pins voor jouw ESP32)
i2c = I2C(0, scl=Pin(6), sda=Pin(5), freq=400000)

# Scan de I2C-bus en print de gevonden adressen
devices = i2c.scan()
if devices:
    print('I2C-apparaten gevonden op adressen:')
    for device in devices:
        print(hex(device))
else:
    print('Geen I2C-apparaten gevonden.')
