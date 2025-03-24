import asyncio
from bleak import BleakClient

# Het Bluetooth adres van de ESP32
target_address = "98:F4:AB:6B:D3:2E"  # Vervang dit door het juiste adres van je ESP32
UART_RX_UUID = "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"


async def run():
    while True:
        try:
            async with BleakClient(target_address) as client:
                print(f"Verbonden: {client.is_connected}")

                # Dit is nu binnen de 'async with' blok
                while True:
                    input("Druk op Enter om de LED te toggelen...")
                    await client.write_gatt_char(UART_RX_UUID, b'1')  # Verzend de 'l' toets naar de ESP32
                break  # Als de verbinding lukt, stop de poging
        except Exception as e:
            print(f"Verbinden mislukt, opnieuw proberen: {e}")
            await asyncio.sleep(2)  # Wacht even voor nieuwe poging


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
