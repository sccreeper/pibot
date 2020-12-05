import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Code for motor designed to work with L298N driver.
class motor_L298N:
    #init function
    def __init__(self, data):
        self.PIN1 = data["pin_one"]
        self.PIN2 = data["pin_two"]
        self.PWM1 = data["pin_pwm"]

        self.speed = 100

        GPIO.setup(self.PIN1, GPIO.OUT)
        GPIO.setup(self.PIN2, GPIO.OUT)

        GPIO.setup(self.PWM1, GPIO.OUT)

        #Setup PWM
        self.PWM1_OUT = GPIO.PWM(self.PWM1, 1000)

        #Start PWM
        self.PWM1_OUT.start(100)
    #Make the motor go forward
    def forward(self):
        GPIO.output(self.PIN1, GPIO.LOW)

        GPIO.output(self.PIN2, GPIO.HIGH)

    #Make it go backward
    def backward(self):
        GPIO.output(self.PIN2, GPIO.LOW)

        GPIO.output(self.PIN1, GPIO.HIGH)

    #Make it stop
    def stop(self):

        GPIO.output(self.PIN1, GPIO.LOW)
        GPIO.output(self.PIN2, GPIO.LOW)

    #Speed Function
    def set_speed(self, data):
        self.speed = int(data[0])

        self.PWM1_OUT.ChangeDutyCycle(self.speed)