from flask import Flask, redirect, request, render_template
import time, random
import RPi.GPIO as GPIO

RUNNING = True

#Used for numbering the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#LED class
class RGB_LED:
    #init function
    def __init__(self, pins):
        self.RED_PIN = pins[0]
        self.GREEN_PIN = pins[1]
        self.BLUE_PIN = pins[2]

        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)

        self.RED_OUT = GPIO.PWM(self.RED_PIN, 100)
        self.GREEN_OUT = GPIO.PWM(self.GREEN_PIN, 100)
        self.BLUE_OUT = GPIO.PWM(self.BLUE_PIN, 100)

        self.RED_OUT.start(1)
        self.GREEN_OUT.start(1)
        self.BLUE_OUT.start(1)

    def colour(self, red, green, blue):
        self.RED_OUT.ChangeDutyCycle((red/255)*100)
        self.GREEN_OUT.ChangeDutyCycle((green/255)*100)
        self.BLUE_OUT.ChangeDutyCycle((blue/255)*100)  

#Functioon for a normal non RGB LED
class LED:
    #init function
    def __init__(self, pin):
        self.PIN_OUT = pin

        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.PIN_OUT, GPIO.HIGH)
    def off(self):
        GPIO.output(self.PIN_OUT, GPIO.LOW)
        
normal_led = LED(2)

main_led = RGB_LED([17,27,22])


try:
    while True:
        normal_led.on()
        main_led.colour(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        time.sleep(0.25)
        main_led.colour(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        normal_led.off()
        time.sleep(0.25)
except KeyboardInterrupt:        
    time.sleep(10)

    GPIO.cleanup()

"""
app = Flask(__name__)

@app.route('/')
def web_index():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
"""
