#!/usr/bin/python3
from sense_hat import SenseHat
from picamera import PiCamera
from time import sleep
from time import time
from csv import writer
import math
import logging
import random

def LED(Brightness):
    e = [Brightness, Brightness, Brightness]
    image = [
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e,
    e,e,e,e,e,e,e,e
    ]
    sense.set_pixels(image)

def random_color():
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

def LED_flag():
    r= (255, 0, 0) 
    b= (0, 0, 255) 
    t= (255,255,255)
    image = [
    b,b,t,b,r,r,r,r,
    t,b,t,t,t,t,t,t,
    b,t,b,b,r,r,r,r,
    t,t,t,t,t,t,t,t,
    r,r,r,r,r,r,r,r,
    t,t,t,t,t,t,t,t,
    r,r,r,r,r,r,r,r,
    t,t,t,t,t,t,t,t, 
    ]    
    sense.set_pixels(image)

def LED_Indications(Color):
    sense.set_pixel(0,0, Color) #light up the top-right pixel to green, blue, or red to indicate success/failures

GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
NONE = (0, 0, 0)
REC_TIME_SEC = 60
SAMPLES_PER_SEC = 120
sense = SenseHat()
camera = PiCamera()
camera.rotation = 270

LED_Indications(BLUE)
#while not ready_to_start():
#    print("Waiting")
#    sleep(1)

curr_time = time()
g_sample = 0
LED(255)
camera.resolution = (1280,720)
camera.framerate = 60  #15ms frames
camera.start_preview()
#Use this to convert to MP4 ffmpeg -framerate 60 -i video.h264  -c copy video5.mp4
try:
    camera.start_recording(f'video/{curr_time:.0f}.h264',format='h264',bitrate=2000000)
    LED_Indications(GREEN) #if the recording works, show green
except PiCameraError:
    LED_Indications(RED) #if the recording fails, show red


while True:
    start_time = time()
    end_time = start_time + REC_TIME_SEC
    blink_timer = 0

    with open(f'data/{curr_time:.0f}_data.csv', 'w', newline='') as f:
        data_writer = writer(f)
        data_writer.writerow(['Time','Accel X','Accel Y','Accel Z','Temp','Pressure','Humidity'])

        while (curr_time < end_time):
          #  camera.annotate_text = "annotation #%s" #% i
            raw = sense.get_accelerometer_raw()
            temp = sense.get_temperature()
            press = sense.get_pressure()
            curr_time = time()
            camera.annotate_text = "Sec:{sec:.3f}".format(sec = curr_time) + "Temp: %s C" % round(temp, 1) + " x: {x:.2f}, y: {y:.2f}, z: {z:.2f}".format(**raw)
            data_writer.writerow([round(curr_time, 3), round(raw["x"], 2), round(raw["y"], 2), round(raw["z"], 2), round(temp, 2), round(press, 2)])
            if abs(raw["x"])  >= 1:
                g_sample += 1
            #else: 
                #g_sample = 0
            #If we hit 60, it means g force was over 1.5g for about 2 seconds, so activate
            if g_sample >= 60:
               #print('It\'s go time!')
               LED_flag()
            else: 
                #print('False alarm')
                random_color()
            if blink_timer >= 5:
            #    LED_Indications(GREEN)
                blink_timer = 0 #every five readings, blink a green LED
            else:
            #    LED_Indications(NONE) #turn off the green LED unless it is the fith reading
                blink_timer += 1
            if blink_timer >= 5:
                #LED_Indications(GREEN)
                random_color() 
                blink_timer = 0 #every five readings, blink a green LED
            else:
                #LED_Indications(NONE) #turn off the green LED unless it is the fith reading
                blink_timer += 1
        camera.split_recording(f'video/{curr_time:.0f}.h264') #start recording in a new file

camera.stop_recording()
camera.stop_preview()
LED(0)
