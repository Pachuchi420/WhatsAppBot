from cgitb import reset
import subprocess
import os
import random
import pandas as pd
import time as t
import schedule 
from datetime import datetime, timedelta, time


# Global Variables
scriptdir = os.path.dirname(os.path.abspath(__file__))
current_time = datetime.now()
set_time = '08:50'

class sellingList:
    def __init__(self, csvFile, photoPath, end, group, name):
        # Starting Properties
        self.givenFile = csvFile
        self.photoPath = photoPath
        self.end = end
        self.group = group
        self.name = name

        self.index = 0  # initialize the current index to 0
        self.csvFile = os.path.join(scriptdir, self.givenFile)
        self.data = pd.read_csv(self.csvFile, sep=';')
        self.photos = os.path.join(scriptdir, self.photoPath + '/Photo_' + str(self.index) + '.jpeg')

        # Details
        self.product = self.data['Producto'][self.index]
        self.size = self.data['Talla'][self.index]
        self.price = self.data['Precio'][self.index]
        self.status = self.data['Vendido'][self.index]

        # Output
        self.msg = 'Si le interesa este articulo favor de darle reply al mensaje con un "yo".'
        self.command = f"npx mudslide@latest send-image --caption '- {self.product} {self.size} \n- {self.price} pesos \n- {self.msg} \n- ID: {self.index}' {self.group} {self.photos}"

    def nextItem(self):
        self.data = pd.read_csv(self.csvFile, sep=';') # reload file for changes
        self.index += 1  # increment the current index
        if self.index >= self.end:  # reset the current index to 0 if it reaches the end
            self.index = 0
        self.photos = os.path.join(scriptdir, self.photoPath + '/Photo_' + str(self.index) + '.jpeg')
        self.product = self.data['Producto'][self.index]
        self.size = self.data['Talla'][self.index]
        self.price = self.data['Precio'][self.index]
        self.status = self.data['Vendido'][self.index]
        self.command = f"npx mudslide@latest send-image --caption '- {self.product} {self.size} \n- {self.price} pesos \n- {self.msg} \n- ID: {self.index}' {self.group} {self.photos}"


    def run(self):
        
        # If sold or reserved skip to next 
        if self.status == 1 or self.status == 1.0:
            self.nextItem()
            print('\nPRODUCT SOLD, SKIPPING....')
            self.run()

        # Prints info
        print(f"\n\n---> Product Info for {self.name} <---")
        print(f"Group: {self.group}")
        print(f"ID Number: {self.index}")
        print(f"Product: {self.product}")
        subprocess.run(self.command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("Message Sent at ->", current_time)

        # After sending message, get to the next item
        self.nextItem()

        
         
def startInterval(every, timeDelta, list):
    schedule.every(every).seconds.until(timedelta(seconds=timeDelta)).do(list)

def main():
    print('--> SCHEDULE STARTS <--')
    list1 = sellingList("Sell1.csv", "Fotos1", 73, "5215528990554-1601327646@g.us", "Sell1")
    list2 = sellingList("Sell2.csv", "Fotos2", 46, "5215528990554-1601327646@g.us", "Sell2")
    startInterval(600, 22800, list1.run)
    print("\n------------------ NEXT SELL BLOCK ------------------")
    startInterval(900, 22800, list2.run)
    print("\n------------------ NEXT SELL BLOCK ------------------")


    

print('Whatsapp Uploader V3')
print(f'Time start: {set_time}')
schedule.every().day.at(set_time).do(main)

while True:
    schedule.run_pending()
    t.sleep(1)
