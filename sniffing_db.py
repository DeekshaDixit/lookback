import serial

import pymysql
import time
conn=pymysql.connect(host="localhost", user="root", passwd="", db="mac")
mycursor=conn.cursor()
ser = serial.Serial('COM4', 115200, timeout=0)
 
while 1:
 try:
  combined = ser.readline()
  mac= combined[:17]
  rssi= combined[17:20]
  print mac
  try:
   print(int(rssi))
   try:
     mycursor.execute("INSERT INTO sniffing(macaddress,RSSI) VALUES(%s,%s)",
                      (mac,rssi))
     print(">Data inserted")
     conn.commit()
   except pymysql.IntegrityError as err:
     pass
   time.sleep(0.1)
  except ValueError:
   pass  
  time.sleep(0.1)
 except ser.SerialTimeoutException:
  print('Data could not be read')
  time.sleep(0.1)
