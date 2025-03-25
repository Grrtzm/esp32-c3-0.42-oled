# This program is meant to work with "BLE_Read_Button.py" running on the ESP32-C3

import asyncio
from bleak import BleakClient, BleakScanner

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"  # Gebruik de TX karakteristiek voor meldingen


async def notification_handler(sender, data):
    print(f"Button state: {data.decode('utf-8')}")


async def connect_to_device(device):
    async with BleakClient(device) as client:
        print(f"Connected to {device.name}")

        # Gebruik de services eigenschap in plaats van get_services methode
        services = client.services
        for service in services:
            print(f"Service: {service.uuid}")
            for char in service.characteristics:
                print(f"  Characteristic: {char.uuid}")

        # Start notification
        await client.start_notify(UART_TX_CHAR_UUID, notification_handler)
        try:
            while True:
                await asyncio.sleep(1)  # Keep the connection alive
        except asyncio.CancelledError:
            await client.stop_notify(UART_TX_CHAR_UUID)
            print("Disconnected")


async def main():
    while True:
        print("Scanning for devices...")
        devices = await BleakScanner.discover()
        for device in devices:
            print(f"Found device: {device.name} ({device.address})")
            if device.name and "ESP32_UART" in device.name:
                print(f"ESP32_UART found: {device.name} ({device.address})")
                await connect_to_device(device)
                break
        await asyncio.sleep(5)  # Wait before scanning again


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Program terminated by user")