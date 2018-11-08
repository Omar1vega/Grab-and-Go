#!/usr/bin/env python
########################################################################
# Filename    : I2CLCD1602.py
# Description : Use the LCD display data
# Author      : freenove
# modification: 2017/04/18
########################################################################
from PCF8574 import PCF8574_GPIO
from Adafruit_LCD1602 import Adafruit_CharLCD
import RPi.GPIO as GPIO
import smbus
import math
import smtplib
import time



from time import sleep, strftime
from datetime import datetime

buttonPin = 12
state = True
light = 0.0
thermAddress = 0x48
bus = smbus.SMBus(1)
cmd = 0x40
trigPin = 16
echoPin = 18
MAX_DISTANCE = 220          #define the maximum measured distance
timeOut = MAX_DISTANCE*60   #calculate timeout according to the maximum measured distance

def checkLight():
    global light
    value = analogRead(1)
    if (light+50<value or light-50>value):
        voltage = value / 255.0 * 3.3
        return voltage
    return 0

def pulseIn(pin,level,timeOut): # function pulseIn: obtain pulse time of a pin
    t0 = time.time()
    while(GPIO.input(pin) != level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    t0 = time.time()
    while(GPIO.input(pin) == level):
        if((time.time() - t0) > timeOut*0.000001):
            return 0;
    pulseTime = (time.time() - t0)*1000000
    return pulseTime
    
def getSonar():     #get the measurement results of ultrasonic module,with unit: cm
    GPIO.output(trigPin,GPIO.HIGH)      #make trigPin send 10us high level 
    time.sleep(0.00001)     #10us
    GPIO.output(trigPin,GPIO.LOW)
    pingTime = pulseIn(echoPin,GPIO.HIGH,timeOut)   #read plus time of echoPin
    distance = pingTime * 340.0 / 2.0 / 10000.0     # the sound speed is 340m/s, and calculate distance
    return distance
    
def setup():
    print('Program is starting...')
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(trigPin, GPIO.OUT)   #
    GPIO.setup(echoPin, GPIO.IN)    #
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
def sendText(message,recipient):
    username = "eecs113team30@gmail.com"     ##enter gmail username and password to send text to mobile
    password = "team30rpi"
    
    msg = """From: %s \nTo: %s\nSubject:ALERT\n%s""" % (username, recipient, message)
    print (msg)
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(username,password)
    server.sendmail(username, recipient,msg)
    print ("email sent")
    server.quit()

def analogRead(channel):
    return bus.read_byte_data(thermAddress,cmd+channel)

def analogWrite(value):
    bus.write_byte_data(address,cmd,value)
    return

def buttonEvent(channel):
    print('buttonEvent GPIO%d'%channel)
    global state
    state = not state

def getAmbientTemp():
    global state
    value = analogRead(0)
    voltage = value/255.0 * 3.3
    Rt = 10 * voltage /(3.3-voltage)
    tempK = 1/(1/(273.15 + 25) + math.log(Rt/10)/3950.0) #calculate temperature (Kelvin)
    tempC = tempK -273.15		#calculate temperature (Celsius)
    tempF = 9.0 / 5.0 * tempC + 32

    return tempF

def get_time_now():     # get system time
    return datetime.now().strftime('%b %-d %X')
def checkDistance(distance):
    return distance<=20 and distance>0

def homeMode():
     message = 'Temp:'+ str(round(getAmbientTemp()))+'\n'+get_time_now()
     lcd.setCursor(0,0)  # set cursor position
     lcd.message(message)   # display the time
     print(message)

     global personAlerted 
     personAlerted = False

     sleep(1)

personAlerted = False
counter = 0
def awayMode():
    global personAlerted
    message = 'Alarm\nActive'
    lcd.setCursor(0,0)
    lcd.message(message)
    ldif = checkLight()    
    distance = getSonar()

    
    if (checkDistance(distance) or ldif):
        if(not personAlerted):
            personAlerted = True
            print"Sending Alarm..."
            txt = "ALERT:\n"
            if (ldif):
                txt += "Light detected voltage %.2f\n"%(ldif)
            if (checkDistance(distance)):
                txt += "Motion %.2f cm from sensor"%(distance)
            sendText(txt,"5623217144@tmomail.net")
            print "The distance is : %.2f cm"%(distance)


    time.sleep(1)
    
def loop():
    global state
    global light
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    GPIO.add_event_detect(buttonPin,GPIO.FALLING,callback = buttonEvent, bouncetime=300)

    flag = True
    while(True):
        if(state):
            flag = True
            light = 0
            homeMode()
        else:

            if(flag):
                lcd.clear()
                analogRead(1)
                light = analogRead(1)
                print("Initial light voltage  =", light)
                flag = not flag
            awayMode()

        #lcd.clear()
       
        
def destroy():
    lcd.clear()
    GPIO.cleanup()

PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print 'I2C Address Error !'
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print 'Program is starting ... '
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()

