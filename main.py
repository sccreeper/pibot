from flask import Flask, redirect, request, render_template, abort
import time, random
import robot
import RPi.GPIO as GPIO
        
#motor_A = robot.motor(
#motor_B = robot.motor(

normal_led = robot.LED(2)

main_led = robot.RGB_LED([17,27,22])

"""
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
        #normal_led.on()
        #main_led.colour(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #time.sleep(0.25)
        #main_led.colour(random.randint(0,255), random.randint(0,255), random.randint(0,255))
        #normal_led.off()
        #time.sleep(0.25)
except KeyboardInterrupt:        
    time.sleep(10)

    GPIO.cleanup()

"""
app = Flask(__name__)

@app.route('/')
def web_index():
    return render_template('index.html')

@app.route('/rgb', methods=['POST'])
def web_rgb():
    if request.method == 'POST':
        main_led.colour(int(request.form['LED_R']), int(request.form['LED_G']), int(request.form['LED_B']))
        return redirect('/')
    else:
        return abort(500)

@app.route('/stop_server', methods=['POST'])
def web_stop_server():
    if request.method == 'POST':
        if request.form['PASS'] == 'topSecretPassword':
            GPIO.cleanup()
            exit()
        else:
            return redirect('/')
    else:
        abort(500)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
