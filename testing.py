#!/usr/bin/python3
from sense_hat import SenseHat
#from picamera import PiCamera
from time import sleep
from time import time
from csv import writer
import math
import logging
import random


def LED2():
    # random.int picks a number between 0, and 255.
    # typed in random.random.int 3 times to get a variable and then wrote it in rows.
    # 
    e = random.randint(0,255),random.randint(0,255),random.randint(0,255)
    t = (255,255,255) 
    image = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,t,t,e,e,e,
    e,e,e,t,t,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    t,t,t,t,t,t,t,t
    ]
    sense.set_pixels(image)


def LED_Indications(Color):
    sense.set_pixel(0,0, Color) #light up the top-right pixel to green, blue, or red to indicate success/failures

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0) 
NONE = (0, 0, 0)
REC_TIME_SEC = 60
SAMPLES_PER_SEC = 120
sense = SenseHat()



curr_time = time()
sense.show_message("GO", .1,GREEN,NONE)
sense.show_message("SBS", .1,RED,NONE)
sense.show_message("ROCKET", .1,YELLOW,NONE)
sense.show_message("CLUB", .1,[0,0,255],NONE)
#LED2 means change color, sleep rests the program 
while True:
    LED2()
    sleep(0.25)
  
raw = sense.get_accelerometer_raw()
temp = sense.get_temperature()
press = sense.get_pressure()
curr_time = time()

print("Raw accel is", raw)
print("Temp is ", temp)
print("Pressure is ", press)

LED(0)
