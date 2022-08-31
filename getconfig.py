#Imports the OS library, allowing extra file information to be retrieved
import os

class getconfig:
    def __init__(self):
        self.file = open("config.txt")
        self.content = self.file.readlines()
        

    def uuid(self):
        #Example of uuid: DAB91383-B5A1-E29C-B041-BCD562613BDE
        if getconfig().empty() == False:
            #Return the second line of the config file
            return str(self.content[1][:-1])
        else:
            return "Empty Config"
    
    def bluetoothaddress(self):
        #Example of bluetooth address: F2:50:DD:65:3B:FB
        if getconfig().empty() == False:
            #Return the first line of the config file
            return str(self.content[0][:-1])
        else:
            return "Empty Config"
        
          
    def empty(self):
        #Checks if the file size is equal to 0, if so the file is empty and will not have a config filled out
        if os.stat("config.txt").st_size == 0:
            return True
        else:
            return False




