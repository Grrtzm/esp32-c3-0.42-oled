from machine import Pin
import utime

# Definieer de pinnen
led = Pin(8, Pin.OUT)  # Onboard LED op GPIO 8
button = Pin(9, Pin.IN, Pin.PULL_UP)  # BOOT-knop op GPIO 9 (pull-up ingeschakeld)

# Variabelen voor toggle en debounce
led_state = False  # LED begint aan
last_button_state = button.value()
last_debounce_time = 0
debounce_delay = 50  # Debounce tijd in milliseconden

# Zet de LED aan bij start
led.value(led_state)

while True:
    current_time = utime.ticks_ms()
    button_state = button.value()

    # Detecteer state change met debounce
    if button_state != last_button_state:

        if (current_time - last_debounce_time) > debounce_delay:
            # Controleer of knop echt is veranderd
            if button_state == 0 and last_button_state == 1:
                led_state = not led_state  # Toggle LED
                led.value(led_state)

        last_debounce_time = current_time  # Reset debounce timer
        last_button_state = button_state  # Update laatste knopstatus
