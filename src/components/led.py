import RPi.GPIO as GPIO

#Used for numbering the pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Normal LED
class LED:
    #init function
    def __init__(self, data):
        self.PIN_OUT = data['pin']

        GPIO.setup(self.PIN_OUT, GPIO.OUT)

    def on(self):
        GPIO.output(self.PIN_OUT, GPIO.HIGH)
    def off(self):
        GPIO.output(self.PIN_OUT, GPIO.LOW)

#RGB LED class
class RGB_LED:
    #init function
    def __init__(self, data):
        self.RED_PIN = data["red_pin"]
        self.GREEN_PIN = data["blue_pin"]
        self.BLUE_PIN = data["green_pin"]

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
