# Import libraries
import os
import RPi.GPIO as GPIO
import time

from gpiozero import Button, LED
from picamera import PiCamera
from signal import pause
import subprocess
import time
import threading
import calendar
import json
import requests
import schedule

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

p = GPIO.PWM(servoPIN, 50)  # GPIO 17 for PWM with 50Hz
p.start(0)  # Initialization

# GET TOKEN FROM ENV VARIABLE
pushToken = os.getenv("PUSH_BULLET")

camera = PiCamera()
scheduler = schedule.Scheduler()
url_request = "https://api.pushbullet.com/v2/upload-request"
url_push = "https://api.pushbullet.com/v2/pushes"
data_request = {"file_type": "image/jpeg"}
headers_request = {"Content-Type": "application/json",
                   "Access-Token": pushToken}

print("File loaded")

led1 = LED(22)
flash = LED(23)
led2 = LED(27)
button_release = Button(20)
button_onoff = Button(21)
isOpen = False
running = True
hours = ["09:00", "12:00", "16:00", "20:00", "00:00"]

try:
    def sendMessage(title, msg):
        data_push = {"type": "note", "title": str(title), "body": str(
            msg), "email": "wender.lima@gmail.com"}
        requests.post(url_push, json=data_push, headers=headers_request)

    def shot():
        flash.on()
        time.sleep(0.5)
        timestamp = calendar.timegm(time.gmtime())
        filename = ('%s.jpg' % timestamp)

        camera.capture(filename)
        time.sleep(0.5)

        imageRequest = requests.post(
            url_request, json=data_request, headers=headers_request)
        imageReqJson = json.loads(json.dumps(imageRequest.json()))

        files = {"file": open(filename, "rb")}
        time.sleep(0.5)

        flash.off()

        upload = requests.post(imageReqJson["upload_url"], files=files)
        time.sleep(0.3)
        print(upload.status_code)

        data_push = {"type": "file", "file_name": filename,
                     "file_type": imageReqJson["file_type"], "file_url": imageReqJson["file_url"], "email": "wender.lima@gmail.com"}

        push = requests.post(url_push, json=data_push, headers=headers_request)
        time.sleep(0.3)

        print(push.status_code)
        print(push.content)

    def release():
        global p
        print("Release")
        cicleTime = 0.37
        try:
            p.ChangeDutyCycle(2+(70/18))
            time.sleep(cicleTime)
            p.ChangeDutyCycle(0)
            time.sleep(0.1)
            p.ChangeDutyCycle(2+(17.05/18))
            time.sleep(cicleTime)
            p.ChangeDutyCycle(0)
            time.sleep(0.1)
            p.ChangeDutyCycle(2+(17.05/18))
            time.sleep(cicleTime)
            p.ChangeDutyCycle(0)

        except Exception as e:
            sendMessage("Erro no feeder", "Erro no release " + str(e))
            time.sleep(1)
            shot()
            time.sleep(1)
            p.ChangeDutyCycle(0)
        finally:
            print("Release finalizado")

    def setInterval(func, time):
        e = threading.Event()
        while not e.wait(time):
            func()

    def looping():
        global running
        if running:
            led2.on()
            scheduler.run_pending()
        else:
            led2.off()

    def onOff():
        print("onOff")
        global running
        running = not running
        print("Running", running)

    def job():
        release()
        shot()

    for hour in hours:
        scheduler.every().day.at(str(hour)).do(job)

    button_release.when_pressed = release
    button_onoff.when_pressed = onOff

    # scheduler.every(5).seconds.do(release)

    led1.on()
    sendMessage("Inicializado", hours)
    shot()
    time.sleep(0.5)

    setInterval(looping, 1)

    print("After interval")
    pause()

except Exception as e:
    print("Oops!", e, "occurred.")

    data_push = {"type": "note", "title": "Erro no feeder",
                 "body": "Erro no feeder, reiniciando" + str(e), "email": "wender.lima@gmail.com"}

    push = requests.post(url_push, json=data_push, headers=headers_request)

    time.sleep(1)

    shot()

    time.sleep(1)

    command = "/usr/bin/sudo /sbin/shutdown -r now"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output = process.communicate()[0]
    print(output)

finally:
    # Clean things up at the end
    led1.off()
    p.stop()
    GPIO.cleanup()
    print("Goodbye!")
