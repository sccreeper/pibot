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

#Function for a normal non RGB LED
class LED:
    #init function
    def __init__(self, pin):
        self.PIN_OUT = pin

        GPIO.setup(pin, GPIO.OUT)

    def on(self):
        GPIO.output(self.PIN_OUT, GPIO.HIGH)
    def off(self):
        GPIO.output(self.PIN_OUT, GPIO.LOW)

#motor class
class motor:
    #init function
    def __init__(self, pin_one, pin_two, pwm_pin):
        self.PIN1 = pin_one
        self.PIN2 = pin_two
        self.PWM1 = pwm_pin

        GPIO.setup(pin_one, GPIO.OUT)
        GPIO.setup(pin_two, GPIO.OUT)

        GPIO.setup(self.PWM1, GPIO.OUT)

        #Setup PWM
        self.PWM1_OUT = GPIO.PWM(self.PWM1, 1000)

        #Start PWM
        self.PWM1_OUT.start(25)
    #Make the motor go forward
    def forward(self, speed):
        self.PWM1_OUT.ChangeDutyCycle(speed)
        GPIO.output(self.PIN1, GPIO.LOW)

        GPIO.output(self.PIN2, GPIO.HIGH)

    #Make it go backward
    def backward(self, speed):
        self.PWM1_OUT.ChangeDutyCycle(speed)
        GPIO.output(self.PIN2, GPIO.LOW)

        GPIO.output(self.PIN1, GPIO.HIGH)

    #Make it stop
    def stop(self):
        self.PWM1_OUT.ChangeDutyCycle(0)

        GPIO.output(self.PIN1, GPIO.LOW)
        GPIO.output(self.PIN2, GPIO.LOW)

    #Speed Function
    def set_speed(self, speed):
        self.PWM1_OUT.ChangeDutyCycle(speed)
