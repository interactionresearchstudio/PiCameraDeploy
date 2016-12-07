#!/usr/bin/env python
import cv2
import json
import time
import datetime

# pi specific imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
# end of imports

# load configuration file
os.chdir("/home/pi/BlankExample")
config = json.load(open("config.json"))

cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)

camera = PiCamera()
camera.resolution = (320,240)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(320,240))
time.sleep(config["camera_warmup"])

# buttons
btn1 = 17
btn2 = 22
btn3 = 23
btn4 = 27
btnShutter = btn1
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(btn1, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn2, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn3, GPIO.IN, GPIO.PUD_UP)
GPIO.setup(btn4, GPIO.IN, GPIO.PUD_UP)

# main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # get new frame
    image = frame.array
    # end of new frame

    cv2.imshow("Output", image)

    # clear buffer
    rawCapture.truncate(0)
    key = cv2.waitKey(10)
    # end of loop

# cleanup
cv2.destroyWindow("Output")
