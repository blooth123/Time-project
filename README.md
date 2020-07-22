# Time-project

### 방범키드 제작(매화 Team)

#제작 목적 및 개념도
```
 자택 및 사업장에서 외출시 사용자가 경비를 위해 만든 방범 키트입니다.
텔레그램으로 외출시 on을 입력해놓으면 인체감지센서를 통해 누군가가 침입했을때 감지되어
사진을 캡쳐하기위해 백색등이 켜지고 시간이지나 적색등을 밝히며 찍힌 사진은 사용자의 텔레그램으로 감지된 시간과 캡처본이
전송됩니다.
```
# 사용된 모듈
- 라즈베리파이 3B+
- 카메라 모듈(캡처기능)
- LED 통합센서 모드(문 외부 상단 설치)
- 스마트 터치 보드

## 개발과정
# 1. 인체감지센서, 카메라
- 라즈베리파이 3B+ 인체 감지 센서 실행, 카메라 모듈에 카메라 촬영 및 캡처 성공
```
#!/usr/bin/python
import RPi.HPIO as GPIO
import time, sys, serial
from picamera impirt picamera 
#import telepot
import telegram 
from telegram.ext import Updater
import logging

GPIO.setmode(GPIO.BCM)

pirpin = 4
GPIO.setup(pirpin, GPIO.IN, GPIO,PUD_UP)
camera = piCamera()
#counter = 1 

while True:
    if GPIO.input(pirpin) == GPIO.LOW:
       try:
           #camera.rotation = 180
           camera.resolution = (2592, 1944)
           camera.framerate = 15
           camera.start_preview()
           camera.brightness = 55
           #time.sleep(1)
           camera.capture('image.jpg')
           #counter = counter + 1
           camera.stop_preview()
           bot = telegram.Bot('1324949291:AAG2ezp_ULGNX6qGELySULM88ZWIxfqQ_o')
           chat_id = 1118932942
           bot.sendMessage(chat_id=chat_id, text= "Motion Detected!")
           #photo = open('./image.jpg','rb')
           #bot.sendphoto(tel_id, photo)
      except:
      cmaera.stop_preview()
  time.sleep(3)
```
## 2. LED
- 라즈베리파이 통합센서 이용하여 인체감지센서를 이용한 LED 조명
```
RGB 색상을 사용
```
```
def sense (update, context) : 
sense = sense Hat()

x = [255, 0, 0]
o = [255, 255, 255]
w = [0, 84, 255]
question_mark = [
o, o, o, o, o, o, o, o, 
o, o, o, o, o, o, o, o, 
o, o, o, x, x, o, o, o,
o, o, x, x, x, x, o, o,
o, o, w, w, w, w, o, o, 
o, o, o, w, w, o, o, o, 
o, o, o, o, o, o, o, o,
o, o, o, o, o, o, o, o
]
sense. set_pixels(question_mark)
time,sleep(2)

sense.clear(255, 0, 0)

def off (update, context) : 

def off (update, context) :
sense = senseHat ()
sense.clear(0, 0, 0)
```
