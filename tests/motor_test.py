import sys
sys.path.append("..")
import robot
import time
import RPi.GPIO as GPIO

motor_A = robot.motor(1,7)
motor_B = robot.motor(8,25)

motor_A.forward()
time.sleep(3)
motor_A.backward()
time.sleep(3)
motor_A.stop()

time.sleep(5)

motor_B.forward()
time.sleep(3)
motor_B.backward()
time.sleep(3)
motor_B.stop()

GPIO.cleanup()

