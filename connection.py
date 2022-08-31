#Imports the required libraries 
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
#UUID to send all data to DAB91383-B5A1-E29C-B041-BCD562613BDE
#https://stackoverflow.com/questions/69326389/bleak-find-device-only-when-runing-bluetoothctl-power-on-scan-on
#D8:1E:E8:E3:F8:6D: Furby





class connect:
    def __init__(self):
        pass


    #A function to scan for the furby
    async def scan(self):
        found = "Furb not found"

        #Using the bleackscanner module nearby discoverable bluetooth devices are detected
        devices = await BleakScanner.discover()

        #Checking through every device that was discovered
        for d in devices:
            #If the device name is "Furby"
            if d.name == "Furby":
                found = d.address

        #Returns "found" which will equal the furbys bluetooth address if the furby is found or alternatively "Furb not found" if the furby is not detected
        return found

    #A function to check connection status with the furby
    async def checkconnection(self, furb):
        print("ok furb is equal to:", furb)
        try:
            async with BleakClient(furb) as client:
                print("Client is connected?: ", client.is_connected)
                return client.is_connected
        except:
            print("Not connected")
            return False
        




