from picamera import PiCamera
from time import sleep, time

camera = PiCamera()

print('previewing')
camera.start_preview()
sleep(5)
camera.stop_preview()

camera.start_preview()
for i in range(5):
    print('picture %s' % i)
    sleep(5)
    camera.capture('/home/pi/Desktop/image0%s.jpg' % round(time()))
camera.stop_preview()

print('recording')
camera.start_preview()
camera.start_recording('/home/pi/Desktop/video.h264')
sleep(5)
camera.stop_recording()
camera.stop_preview()
