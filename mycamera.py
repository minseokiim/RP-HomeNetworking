####mycamera.py
import os
import io
import time
import RPi.GPIO as GPIO
import picamera
import cv2
import numpy as np
trig = 20
echo = 16 # 초음파
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.output(trig, False)
fileName = ""
stream = io.BytesIO()
camera = picamera.PiCamera()
camera.start_preview()
camera.resolution = (320, 240)
time.sleep(1)
def measureDistance(): # 초음파
global trig, echo
time.sleep(1)
GPIO.output(trig, True) # 신호 1 발생
time.sleep(0.1)
GPIO.output(trig, False) # 신호 0 발생
while(GPIO.input(echo) == 0):
pass
pulse_start = time.time() # 신호 1을 받았던 시간
while(GPIO.input(echo) == 1):
pulse_end = time.time() # 신호 0을 받았던 시간
pulse_duration = pulse_end - pulse_start
return 340*100/2*pulse_duration
def takePicture() : #사진 촬영 함수
global fileName, stream, camera
if len(fileName) != 0:
os.unlink(fileName)
stream.seek(0)
stream.truncate()
camera.capture(stream, format='jpeg', use_video_port=True)
data = np.frombuffer(stream.getvalue(), dtype=np.uint8)
image = cv2.imdecode(data, 1)
haar = cv2.CascadeClassifier('./haarCascades/haar-cascadefilesmaster/haarcascade_frontalface_default.xml')
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
faces = haar.detectMultiScale(image_gray,1.1,3)
for x, y, w, h in faces:
cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
takeTime = time.time()
fileName = "./static/%d.jpg" % (takeTime * 10)
cv2.imwrite(fileName, image)
return fileName
if __name__ == '__main__' :
led_status = 0
while(True):
distance = measureDistance()
print("distance=%f" % distance)
name = takePicture()
print("fname= %s" % name)