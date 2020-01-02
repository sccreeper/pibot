import sys
sys.path.append("..")

import time, robot, random

#LED Test Script
normal_led = robot.LED(2)

main_led = robot.RGB_LED([17,27,22])


try:
    colour_completed = True
    while True:
        for i in range(255):
            main_led.colour(i,0,0)
            time.sleep(0.05)
        for i in range(255):
            main_led.colour(255, i, 0)
            time.sleep(0.05)
        for i in range(255):
            main_led.colour(255, 255, i)
            time.sleep(0.05)
        for i in range(255):
            main_led.colour(0,0,i)
            time.sleep(0.05)
        for i in range(255):
            main_led.colour(0, i, 255)
            time.sleep(0.05)
        for i in range(255):
            main_led.colour(i, 255, 255)
            time.sleep(0.05)
        normal_led.on()
        time.sleep(0.25)
        main_led.colour(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        normal_led.off()
        time.sleep(0.25)
except KeyboardInterrupt:        
    time.sleep(10)

    GPIO.cleanup()

