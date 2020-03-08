import http.server
import socketserver
import graffitiModule as gfm
import os
from urllib.parse import urlparse, parse_qs

port = 80

class GraffitiHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        print('\033[32;1m%s\033[0m;' % self.path)
        purl = urlparse(self.path)
        print(purl)
        if purl.path == '/text':
            query = parse_qs(purl.query)
            if not "message" in query:
                self.send_response(400, 'Invalid message')
                self.end_headers()
                return
            print('Got text request: ' + query["message"])
            os.remove('final.png')
            gfm.generate(text=query["message"], out="final.png")
            self.send_response(200)
            self.send_header('content-type', 'image/png')

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", port), GraffitiHandler) as server:
    print('Serving at port %s' % port)
    server.serve_forever()