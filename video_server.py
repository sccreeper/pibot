#See https://blog.ronnyvdb.net/2019/01/20/howto-stream-html5-video-h264-encoded-video-encapsulated-in-mp4-from-the-raspberry-pi-to-any-web-browser/
#This doesn't work. I'm just leaving it in here in hope it gets fixed. Some problem with the GST idk what though.

import subprocess # for piping
from http.server import HTTPServer, BaseHTTPRequestHandler

class RequestHandler(BaseHTTPRequestHandler):
    def _writeheaders(self):
        self.send_response(200) # 200 OK http response
        self.send_header('Content-type', 'video/mp4')
        self.end_headers()

    def do_HEAD(self):
        self._writeheaders()

    def do_GET(self):
        self._writeheaders()

        DataChunkSize = 10000

        command = '(echo "--video boundary--"; raspivid -w 1920 -h 1080 -fps 30 -pf high -n -t 0 -o -;) | gst-launch-1.0 -e -q fdsrc fd=0 ! video/x-h264,width=1920,height=1080,framerate=30/1,stream-format=byte-stream ! h264parse ! mp4mux streamable=true fragment-duration=10 presentation-time=true ! filesink location=/dev/stdout'
        print("running command: %s" % (command, ))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=-1, shell=True)

        print("starting polling loop.")
        while(p.poll() is None):
            print ("looping... ")
            stdoutdata = p.stdout.read(DataChunkSize)
            self.wfile.write(stdoutdata)

        print("Done Looping")

        print("dumping last data, if any")
        stdoutdata = p.stdout.read(DataChunkSize)
        self.wfile.write(stdoutdata)

if __name__ == '__main__':
    serveraddr = ('', 8765) # connect to port 8765
    srvr = HTTPServer(serveraddr, RequestHandler)
    srvr.serve_forever()
