####mqtt.py
import time
import paho.mqtt.client as mqtt
import mycamera # 사진, 거리 정보 보내기
flag = False
def on_connect(client, userdata, flag, rc):
 client.subscribe("facerecognition", qos = 0)
def on_message(client, userdata, msg) :
 global flag
 command = msg.payload.decode("utf-8")
 if command == "action" :
 print("action msg received..")
 flag = True
broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_ip, 1883)
client.loop_start()
while True :
imageFileName = mycamera.takePicture() # 카메라 사진 촬영
print(imageFileName)
client.publish("image", imageFileName, qos=0)
distance=mycamera.measureDistance()
print(distance)
client.publish("거리",distance,qos=0)
flag = False
time.sleep(1)
client.loop_end()
client.disconnect()