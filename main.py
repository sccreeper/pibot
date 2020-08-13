#Server libraries
from flask import Flask, redirect, request, render_template, abort, send_from_directory, Response
import socket
import io
#Other
import time, random
import robot
import RPi.GPIO as GPIO

import os
import subprocess

import json

from datetime import datetime

import atexit
#Camera libraries
from picamera import PiCamera
from camera_pi import Camera

motor_A = robot.motor(1,7, 27)
motor_B = robot.motor(8,25, 22)

normal_led_one = robot.LED(2)
normal_led_two = robot.LED(3)

motor_speed = 50

#main_led = robot.RGB_LED([17,27,22])

#Flask Server
app = Flask(__name__)

debug_log = ''
debug_file_path = ''

def date():
    d = datetime.now()

    return_date = '{}-{}-{}_{}:{}:{}'.format(d.day, d.month, d.year, d.hour, d.minute, d.second)


    return return_date

def date_time():
    d = datetime.now()

    return_time = '{}:{}:{}'.format(d.hour, d.minute, d.second)

    return return_time

def update_log(data):
    global debug_log

    debug_log += data + '\n'

    with open(debug_file_path, "a") as debug_file:
        debug_file.write(data + '\n')

@app.before_request
def web_log():
    global debug_log

    update_log('[{}]'.format(date()) + ' - web - ' + request.full_path + ' - ' + request.remote_addr)

#Index
@app.route('/')
def web_index():
    return render_template('index.html')

#Debug
@app.route('/debug')
def web_debug():
  debugDict = {}

  debugDict['clock'] = {}
  debugDict['temp'] = {}
  debugDict['ip'] = {}

  debugDict['clock']['cpu'] = int(subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode().split('=')[1].replace('\n', '')) / 1000000
  debugDict['clock']['gpu'] = int(subprocess.check_output(['vcgencmd', 'measure_clock', 'h264']).decode().split('=')[1].replace('\n', '')) / 1000000
  debugDict['temp']['soc'] = subprocess.check_output(['vcgencmd', 'measure_temp']).decode().split('=')[1].replace('\n', '')
  debugDict['ip']['host'] = subprocess.check_output(['hostname', '-I']).decode()
  debugDict['ip']['client'] = request.remote_addr
  debugDict['upsince'] = subprocess.check_output(['uptime', '-s']).decode()
  debugDict['log'] = {}
  debugDict['log']['log'] = debug_log
  debugDict['log']['size'] = {}
  debugDict['log']['size']['lines'] = len(debug_log.split('\n'))
  debugDict['log']['size']['kb'] = len(debug_log) / 1024
  debugDict['chart'] = {}
  debugDict['chart']['clock'] = {}
  debugDict['chart']['clock']['cpu'] = int(subprocess.check_output(['vcgencmd', 'measure_clock', 'arm']).decode().split('=')[1].replace('\n', '')) / 1000000
  debugDict['chart']['temp'] = {}
  debugDict['chart']['temp']['soc'] = float(subprocess.check_output(['vcgencmd', 'measure_temp']).decode().split('=')[1].replace('\n', '').replace("'C", ''))

  debugDict['timestamp'] = date_time()

  #print(str(json.dumps(debugDict)))
  return str(json.dumps(debugDict))

#e
#Code for controlling components like the motors and the RGB etc.
@app.route('/control/<component>/', methods=['POST'])
def web_control(component=None):
    global motor_speed

    #print(request.form)

    if request.method == 'POST':
        if component == 'rgb':
            main_led.colour(int(request.form['LED_R']), int(request.form['LED_G']), int(request.form['LED_B']))
            return redirect('/')
        elif component == 'motor':
            try:
                motor_speed = int(request.form['SPEED'])

                motor_A.set_speed(motor_speed)
                motor_B.set_speed(motor_speed)

                return 'Speed changed to {}%'.format(motor_speed)
            except KeyError:
                if len(request.form) == 0:
                    if request.get_json()['DIRECTION'] == 'forward':
                        motor_A.backward(motor_speed)
                        motor_B.forward(motor_speed)
                        return 'Motors going forward'
                    elif request.get_json()['DIRECTION'] == 'backward':
                        motor_A.forward(motor_speed)
                        motor_B.backward(motor_speed)
                        return 'Motors going backward'
                    elif request.get_json()['DIRECTION'] == 'left':
                        motor_A.forward(motor_speed)
                        motor_B.forward(motor_speed)
                        return 'Turning left'
                    elif request.get_json()['DIRECTION'] == 'right':
                        motor_A.backward(motor_speed)
                        motor_B.backward(motor_speed)
                        return 'Turning right'
                    else:
                        motor_A.stop()
                        motor_B.stop()
                        return 'Stopped'
                else:
                    if request.form['DIRECTION'] == 'forward':
                        #Backwards beacause I soldered it wrong, you might want to change this for your own code.
                        motor_A.backward(motor_speed)
                        motor_B.forward(motor_speed)
                        return 'Motors going forward'
                    elif request.form['DIRECTION'] == 'backward':
                        motor_A.forward(motor_speed)
                        motor_B.backward(motor_speed)
                        return 'Motors going backward'
                    elif request.form['DIRECTION'] == 'left':
                        motor_A.forward(motor_speed)
                        motor_B.forward(motor_speed)
                        return 'Turning left'
                    elif request.form['DIRECTION'] == 'right':
                        motor_A.backward(motor_speed)
                        motor_B.backward(motor_speed)
                        return 'Turning right'
                    else:
                        motor_A.stop()
                        motor_B.stop()
                        return 'Stopped'
        elif component == 'headlights':
            if len(request.form) == 0:
                if request.get_json()['STATUS'] == 'on':
                    normal_led_one.on()
                    normal_led_two.on()
                    return 'Headlights on'
                else:
                    normal_led_one.off()
                    normal_led_two.off()
                    return 'Headlights off'
            else:
                if request.form['STATUS'] == 'on':
                    normal_led_one.on()
                    normal_led_two.on()
                    return 'Headlights on'
                else:
                    normal_led_one.off()
                    normal_led_two.off()
                    return 'Headlights off'
        elif component == 'camera':
            if request.form['MODE'] == 'picture':

                camera = PiCamera()

                camera.start_preview()
                time.sleep(5)

                pic_date = date()
                camera.capture('images/image_{}.jpg'.format(pic_date))

                camera.stop_preview()
            return "Took image <a href='/browse_images/image_{}.jpg'>image_{}.jpg</a>".format(pic_date, pic_date)
    else:
        return abort(500)

@app.route('/browse_images/')
def web_browse():
    images = os.listdir('images')

    image_html = ''

    for i in range(len(images)):

        image_html += "\n<a href='/browse_images/" + images[i] + "'>" + images[i] + "</a>"

    return image_html

@app.route('/browse_images/<image>')
def web_view_image(image=None):
    return "<img src='/browse_images/source/" + image + "'/>"

@app.route('/browse_images/source/<image>')
def web_image_source(image=None):
    return send_from_directory('images', image)

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

#Video Stream Stuff
@app.route('/video_feed')
def video_feed():
   """Video streaming route. Put this in the src attribute of an img tag."""
   return Response(gen(Camera()),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/test')
def web_test():
    return render_template('test_page.html')

#Generation function
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        #print(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Stop caching, see: https://stackoverflow.com/a/34067710

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'

    return r

#Debug log
print(debug_log)
debug_file_path = 'logs/{}.log'.format(date())
debug_file = open(debug_file_path, 'w')
debug_file.write(debug_log)
debug_file.close()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)
