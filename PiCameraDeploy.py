import sys
import os
import re

# get input file
inputName = sys.argv[1]
fileWithExtension = os.path.basename(inputName)
fileName, fileExtension = os.path.splitext(fileWithExtension)
print "File name: " + fileName

# open contents of input file
macFile = open(inputName, 'r')
contents = macFile.read()
macFile.close()

# replacements

piBash = """#!/usr/bin/env python
"""

piImportsAndConfigFile ="""# pi specific imports
from picamera.array import PiRGBArray
from picamera import PiCamera
import RPi.GPIO as GPIO
# end of imports

# load configuration file
os.chdir("/home/pi/""" + fileName + """")
config = json.load(open("config.json"))"""

contents = re.sub(r'# configuration file.*?# end of configuration file', piImportsAndConfigFile, contents, flags=re.DOTALL)

piWindowSettings = """cv2.namedWindow("Output", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Output", cv2.WND_PROP_FULLSCREEN, 1)"""

contents = re.sub(r'# window.*?# end of window', piWindowSettings, contents, flags=re.DOTALL)

piCameraAndButtonSettings = """# camera
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
GPIO.setup(btn4, GPIO.IN, GPIO.PUD_UP)"""

contents = re.sub(r'# camera.*?# end of camera', piCameraAndButtonSettings, contents, flags=re.DOTALL)

piMainLoopAndFrame = """# main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # get new frame
    image = frame.array
    # end of new frame"""

contents = re.sub(r'# main loop.*?# end of new frame', piMainLoopAndFrame, contents, flags=re.DOTALL)

piEndOfLoop = """# clear buffer
    rawCapture.truncate(0)
    key = cv2.waitKey(10)
    # end of loop"""

contents = re.sub(r'# wait for keys.*?# end of loop', piEndOfLoop, contents, flags=re.DOTALL)

newContents = piBash + contents
directory = os.path.dirname(inputName)
outputName = directory + "/" + fileName + "-pi.py"

outputFile = open(outputName, 'w')
outputFile.write(newContents)
print "Python script deployed successfully."
