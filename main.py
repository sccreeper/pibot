#Server libraries
from flask import Flask, redirect, request, render_template, abort, send_from_directory, Response
import socket 
import io
#Other 
import time, random
import robot
import RPi.GPIO as GPIO
import os
from datetime import datetime
#Camera libraries
from picamera import PiCamera
from camera_pi import Camera
        
motor_A = robot.motor(1,7)
motor_B = robot.motor(8,25)

normal_led_one = robot.LED(2)
normal_led_two = robot.LED(3)

#main_led = robot.RGB_LED([17,27,22])

#Flask Server
app = Flask(__name__)


def date():
    d = datetime.now()

    return_date = '{}-{}-{}_{}{}{}'.format(d.day, d.month, d.year, d.hour, d.minute, d.second)
    
    
    return return_date

#Index
@app.route('/')
def web_index():
    return render_template('index.html')

#e
#Code for controlling components like the motors and the RGB etc.
@app.route('/control/<component>/', methods=['POST'])
def web_control(component=None):
    if request.method == 'POST':
        if component == 'rgb':
            main_led.colour(int(request.form['LED_R']), int(request.form['LED_G']), int(request.form['LED_B']))
            return redirect('/')
        elif component == 'motor':
            if request.form['DIRECTION'] == 'forward':
                #Backwards beacause I soldered it wrong, you might want to change this for your own code.
                motor_A.backward()
                motor_B.forward()
                return 'Motors going forward'
            elif request.form['DIRECTION'] == 'backward':
                motor_A.forward()
                motor_B.backward()
                return 'Motors going backward'
            elif request.form['DIRECTION'] == 'left':
                motor_A.forward()
                motor_B.forward()
                return 'Turning left'
            elif request.form['DIRECTION'] == 'right':
                motor_A.backward()
                motor_B.backward()
                return 'Turning right'
            else:
                motor_A.stop()
                motor_B.stop()
                return 'Stopped'
        elif component == 'headlights':
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
                   
#Generation function
def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)

