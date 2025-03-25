import asyncio
from bleak import BleakScanner


# Callbackfunctie voor gedetecteerde advertenties
def advertisement_callback(device, advertisement_data):
    # Print de naam van het apparaat en de advertentiegegevens
    print(f"Apparaat gevonden: {device.name}")
    print(f"Advertentiegegevens: {advertisement_data}")


# Asynchrone functie voor scannen naar BLE-apparaten
async def scan_for_advertisements():
    # Start de scan voor 10 seconden
    print("🔍 Scannen gestart...")
    scanner = BleakScanner()
    # Registreer de callback voor gedetecteerde apparaten
    scanner.register_detection_callback(advertisement_callback)
    await scanner.start()

    # Wacht 10 seconden voordat de scan stopt
    await asyncio.sleep(10)
    await scanner.stop()
    print("Scan afgerond.")


# Start de scan
asyncio.run(scan_for_advertisements())
