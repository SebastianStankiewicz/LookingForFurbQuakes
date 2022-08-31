#Imports the required libraries 
import threading
import time
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from earthquake import seismic
from connection import connect
import nest_asyncio
from getconfig import getconfig

#https://pypi.org/project/nest-asyncio/ explains why the line below is required
nest_asyncio.apply()


if getconfig().empty() == False:
    #Fetches infomation from the config file
    MODEL_NBR_UUID = getconfig().uuid()
    furb = getconfig().bluetoothaddress()
else:
    print("Please fill in the config file. Closing in 5 seconds.")
    time.sleep(5)
    quit


#Current id is used to store the previous earthquakes ID so a value of 0 is given at the start as python requires variables to be assigned before referenced but in reality could be equal to anything
currentid = "0"

#Ensures the furby starts in a wake lock
stopidling = False





def scanforfurby():
    found = False
    #Repeat until the furby is discoverable
    while found == False:
        address = asyncio.run(connect().scan())
        print(address)
        if address != "Furb not found":
            found = True
            #Run the main() loop function
            main()
            print("Done!")
            


#https://www.mtu.edu/geo/community/seismology/learn/earthquake-measure/magnitude/
def newquake(magnitude):
    if float(magnitude) <= 2.5:
        #Usually not felt, but can be recorded by seismograph.
        #musical fart, laugh
        return b"\x14\xE4\x08\xFF", b"\x10\x00\x07\x00\x00\x00"
    elif float(magnitude) <= 5.4:
        #Often felt, but only causes minor damage.
        #fart fanfare "oo sha boo nee"
        return b"\x14\x4E\x03\xFC", b"\x10\x00\x07\x00\x00\x01"
    elif float(magnitude) <= 6.0:
        #Slight damage to buildings and other structures.
        #straining, long fart
        return b"\x14\x03\xFC\xFC", b"\x10\x00\x07\x01\x00\x02"
    elif float(magnitude) <= 6.9:
        #May cause a lot of damage in very populated areas.
        #long fart
        return b"\x14\x03\xFC\x31", b"\x10\x00\x07\x02\x00\x00"
    elif float(magnitude) <= 7.9:
        #Major earthquake. Serious damage.
        #chicken noise, fart "meow"
        return b"\x14\xF8\xFC\x03", b"\x10\x00\x07\x01\x01\x01"
    else:
        #Great earthquake. Can totally destroy communities near the epicenter.
        #musical fart "triple threat"
        return b"\x14\xE0\x84\x02", b"\x10\x00\x07\x00\x00\x04"
        
    

#Function to get latest earthquake
def getquakes():
    global currentid, stopidling, latest
    try:
        #latest[0] is the id given to the quake to uniquely  identify each earthquake and latest[1] is the magnitude
        latest = seismic().fetchdata()
        
        #If the latest earthquake does not equal the previous earthquake it means a new earthquake has occurred 
        if latest[0] != currentid and latest[1] != None:
            print("NEW QUAKE")
            
            #Stopidling = True tells the furby to stop its wake lock
            stopidling = True
            currentid = latest[0]
        #Repeat the function
        threading.Timer(5, getquakes).start()
    except Exception as e:
        #If an error occurs fetching seismic activity print the error
        print(e)


#This is the main furby loop that is responsible for handling the furbys actions and is constantly  looping
async def furbymain(furb):
    try:
        async with BleakClient(furb) as client:
            model_number = await client.read_gatt_char(MODEL_NBR_UUID)
            #Due to python limitations, for some reason I could not pass commands to the furby through more than one asynchronous function so all actions had to be handled through one asynchronous function
            print("RUNNNING THE FURBY ACTION LOOP")
            #Repeat forever
            while True:
                try:
                    #Retreive the action to be performed  by the furby from the actionhub() function
                    action = actionhub()
                    print("action: ", action)
                    await asyncio.sleep(3.0)
                    await client.write_gatt_char(MODEL_NBR_UUID, action[1])
                    await client.write_gatt_char(MODEL_NBR_UUID, action[0])
                except Exception as e:
                    #For if an error occurs
                    print(e)
    except Exception as e:
        #For if an error occurs
        print(e)


def actionhub():
    global stopidling
    if stopidling == False:
        #return: b"\x14\xFF\x00\x00", b"\xcd\x00" set the antenna  to red and the eyes of the furby to black, so acts as a wake lock
        #b"\x14\xFF\x00\x00" - Red antenna
        #b"\xcd\x00" - Black eyes
        return b"\x14\xFF\x00\x00", b"\xcd\x00" 
    else:
        #If a dance has been triggered  it will pass the 
        stopidling = False
        #Dance equals the action for the furby to do and this is determined by the earthquakes magnitude (latest[1]) which is passed into the newquake function
        dance = newquake(latest[1])
        return dance
        
        
        


def main():
    #This runs once the furby has been detected and a connection established
    print("Starting main program as furby been detected.")
    print("Starting thread to monitor earthquakes")
    #Creates a thread running the getquakes() funciton
    threading.Timer(5, getquakes).start()
    print("Thread running")
    print("Starting main furby action loop")
    while True:
        #if the furby disconnects  the code will return back to here. The "while True" ensures that the code will consistently  try to connect/reconnect to the furby
        #Runs the furbymain() loop passing the furbys address as furb
        asyncio.run(furbymain(furb))
        print("There was a error lets go again")


#This funciton will run when the program starts and initiates scanforfurby() function
if __name__ == '__main__':
    scanforfurby()
    
