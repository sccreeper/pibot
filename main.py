# Copyright (c) 2020 <Oscar Peace>
#
# GNU GENERAL PUBLIC LICENSE
#    Version 3, 29 June 2007
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Server libraries
from flask import Flask, redirect, request, render_template, abort, send_from_directory, Response, make_response
import socket
import io
# Other
import time
import random
import uuid
import robot
import RPi.GPIO as GPIO

import os
import subprocess

import json

from datetime import datetime

#import atexit
# Camera libraries
from picamera import PiCamera
from camera_pi import Camera

motor_A = robot.motor(1, 7, 27)
motor_B = robot.motor(8, 25, 22)

normal_led_one = robot.LED(2)
normal_led_two = robot.LED(3)

motor_speed = 50

#main_led = robot.RGB_LED([17,27,22])

# Flask Server
app = Flask(__name__)

debug_log = ''
debug_file_path = ''
previous_entry = ''
previous_entry_amount = 0

login_tokens = []

# Configurable GPIO pins
config_gpio = [2, 3, 4, 17, 27, 22, 10, 9, 11, 0, 5, 6, 13,
               19, 26, 14, 15, 18, 23, 24, 25, 8, 7, 1, 12, 16, 20, 21]
GPIO.setmode(GPIO.BCM)

# Util functions


def date():
    d = datetime.now()

    return_date = '{}-{}-{}_{}:{}:{}'.format(d.day,
                                             d.month, d.year, d.hour, d.minute, d.second)

    return return_date


def date_time():
    d = datetime.now()

    return_time = '{}:{}:{}'.format(d.hour, d.minute, d.second)

    return return_time


def read_file(path):
    with open(path, 'r') as file:
        return file.read()

def write_file(path, data):
    with open(path, 'w') as file:
        return file.write(data)


def update_log(data, type):
    global debug_log, previous_entry, previous_entry_amount

    debug_log += '[{}]'.format(date()) + ' - {} - {} \n'.format(type, data)

    if ' - {} - {} \n'.format(type, data) == previous_entry:
        lines = open(debug_file_path).read().splitlines()
        lines[len(lines) - 1] = '[{}][{}]'.format(date(),
                                                  previous_entry_amount) + ' - {} - {} \n'.format(type, data)

        lines2 = open(debug_file_path, 'w')
        lines2.write("\n".join(lines))

        lines2.close()
        # lines.close()

        previous_entry_amount += 1
    else:
        with open(debug_file_path, "a") as debug_file:
            debug_file.write('[{}]'.format(date()) +
                             ' - {} - {} \n'.format(type, data))
        previous_entry = ' - {} - {} \n'.format(type, data)
        previous_entry_amount = 0

def logged_in(request):
    global login_tokens

    if request.cookies.get('t') == None:
        return False

    if request.cookies.get('t') in login_tokens:
        return True
    else:
        return False
@app.before_request
def web_log():
    global debug_log

    if 'android' in request.headers.get('User-Agent').lower():
        update_log(request.full_path + ' - ' + request.remote_addr, 'app')
    else:
        update_log(request.full_path + ' - ' + request.remote_addr, 'web')

# Index
@app.route('/')
def web_index():
    if logged_in(request):
        return render_template('index.html')
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def web_login():
    global login_tokens

    if request.form['pass'] == config['pass']:
        #Generate ID

        while True:
            token = uuid.uuid4()

            if token in login_tokens:
                continue
            else:
                break

        resp = make_response(redirect('/'))
        resp.set_cookie('t', str(token))

        login_tokens.append(str(token))

        return resp
    else:
        return render_template('login.html', message='Incorrect password')



# Debug
@app.route('/debug')
def web_debug():
    debugDict = {}

    debugDict['clock'] = {}
    debugDict['temp'] = {}
    debugDict['ip'] = {}

    debugDict['clock']['cpu'] = int(subprocess.check_output(
        ['vcgencmd', 'measure_clock', 'arm']).decode().split('=')[1].replace('\n', '')) / 1000000
    debugDict['clock']['gpu'] = int(subprocess.check_output(
        ['vcgencmd', 'measure_clock', 'h264']).decode().split('=')[1].replace('\n', '')) / 1000000
    debugDict['temp']['soc'] = subprocess.check_output(
        ['vcgencmd', 'measure_temp']).decode().split('=')[1].replace('\n', '')
    debugDict['ip']['host'] = subprocess.check_output(
        ['hostname', '-I']).decode()
    debugDict['ip']['client'] = request.remote_addr
    debugDict['ip']['ssid'] = subprocess.check_output(['iwgetid']).decode()

    debugDict['upsince'] = subprocess.check_output(['uptime', '-s']).decode()
    debugDict['log'] = {}
    debugDict['log']['log'] = "\n".join(debug_log.split('\n')[-32:])
    debugDict['log']['size'] = {}
    debugDict['log']['size']['lines'] = len(debug_log.split('\n'))
    debugDict['log']['size']['kb'] = os.path.getsize(debug_file_path) / 1024
    debugDict['chart'] = {}
    debugDict['chart']['clock'] = {}
    debugDict['chart']['clock']['cpu'] = int(subprocess.check_output(
        ['vcgencmd', 'measure_clock', 'arm']).decode().split('=')[1].replace('\n', '')) / 1000000
    debugDict['chart']['temp'] = {}
    debugDict['chart']['temp']['soc'] = float(subprocess.check_output(
        ['vcgencmd', 'measure_temp']).decode().split('=')[1].replace('\n', '').replace("'C", ''))

    debugDict['pinouts'] = {}
    debugDict['pinouts']['left'] = []
    debugDict['pinouts']['right'] = []
    # Get pinoutss
    for i in range(20):
        try:
            debugDict['pinouts']['left'].append(GPIO.input(i))
        except RuntimeError:
            debugDict['pinouts']['left'].append(None)

    for i in range(20, 40):
        try:
            debugDict['pinouts']['right'].append(GPIO.input(i))
        except RuntimeError:
            debugDict['pinouts']['right'].append(None)

    debugDict['timestamp'] = date_time()

    # print(str(json.dumps(debugDict)))
    return str(json.dumps(debugDict))


@app.route('/log')
def web_log_plain():
    return '<pre>{}</pre>'.format(debug_log)

# e
# Code for controlling components like the motors and the RGB etc.


@app.route('/control/<component>/', methods=['POST'])
def web_control(component=None):
    global motor_speed

    # print(request.form)

    if request.method == 'POST':
        if component == 'rgb':
            main_led.colour(int(request.form['LED_R']), int(
                request.form['LED_G']), int(request.form['LED_B']))
            return redirect('/')
        elif component == 'motor':
            try:
                if len(request.form) == 0:
                    motor_speed = int(request.get_json()['SPEED'])

                    motor_A.set_speed(motor_speed)
                    motor_B.set_speed(motor_speed)

                    return 'Speed changed to {}%'.format(motor_speed)

                else:
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
                        # Backwards beacause I soldered it wrong, you might want to change this for your own code.
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

                camera.hflip = True
                camera.vflip = True

                camera.start_preview()
                time.sleep(1.5)

                pic_date = date()
                camera.capture('images/image_{}.jpg'.format(pic_date))

                camera.stop_preview()
                camera.close()
            return "Took image <a href='/browse_images/image_{}.jpg'>image_{}.jpg</a>".format(pic_date, pic_date)
    else:
        return abort(500)


@app.route('/browse_images/')
def web_browse():
    images = os.listdir('images')

    image_html = ''

    for i in range(len(images)):

        image_html += "\n<a href='/browse_images/" + \
            images[i] + "'>" + images[i] + "</a>"

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
        if request.form['PASS'] == config['pass']:
            GPIO.cleanup()
            exit()
        else:
            return redirect('/')
    else:
        abort(500)

# Video Stream Stuff


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/test')
def web_test():
    return render_template('test_page.html')

#Settings
@app.route('/settings')
def web_settings():

        if logged_in(request):
            return render_template('settings.html', password=config['pass'], port=config['port'])
        else:
            return redirect('/')

@app.route('/settings_update', methods=['POST'])
def web_settings_update():
    global config

    new_config = {}

    new_config['pass'] = request.form['pass']
    new_config['port'] = request.form['port']

    write_file('config.json', json.dumps(new_config, indent=4, sort_keys=True))
    config = new_config

    return redirect('/settings')

@app.route('/logout')
def web_logout():
    global login_tokens

    login_tokens.remove(request.cookies.get('t'))

    resp = make_response(render_template('login.html', message='Logged out successfully.'))
    resp.set_cookie('token', '')

    return resp

@app.route('/about')
def web_about():
    return render_template('about.html')

@app.route('/about/license')
def web_about_license():
    return "<pre>" + read_file('LICENSE') + "</pre>"

# Generation function


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        # print(frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Stop caching, see: https://stackoverflow.com/a/34067710


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


# Debug log
print(debug_log)
debug_file_path = 'logs/{}.log'.format(date())
debug_file = open(debug_file_path, 'w')
debug_file.write(debug_log)
debug_file.close()

# Config json
config = json.loads(read_file('config.json'))

if __name__ == '__main__':
    update_log('Server starting!', 'info')
    app.run(debug=True, host='0.0.0.0', port=config['port'], threaded=True)
