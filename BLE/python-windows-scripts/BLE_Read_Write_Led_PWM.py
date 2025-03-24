import asyncio
from bleak import BleakClient, BleakScanner

UART_SERVICE_UUID = "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
UART_TX_CHAR_UUID = "6E400002-B5A3-F393-E0A9-E50E24DCCA9E"
UART_RX_CHAR_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


async def notification_handler(sender, data):
    print(f"Current PWM value: {data.decode('utf-8')}")


async def connect_to_device(device):
    async with BleakClient(device) as client:
        print(f"Connected to {device.name}")

        # Start notification
        await client.start_notify(UART_TX_CHAR_UUID, notification_handler)

        # Read the current PWM value
        await asyncio.sleep(1)  # Wait for the first notification
        print("Reading current PWM value...")

        # Main loop to read and write PWM value
        while True:
            new_pwm_value = input("Enter new PWM value (0-1023): ")
            await client.write_gatt_char(UART_RX_CHAR_UUID, new_pwm_value.encode('utf-8'))
            await asyncio.sleep(1)  # Wait for the notification to confirm the new value


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