import http.server
import socketserver
import graffitiModule as gfm
import os
from urllib.parse import urlparse, parse_qs

port = 80

def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

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
            print('Got text request: ' + query["message"][0])
            #os.remove('final.png')
            trim = True
            if "trim" in query:
                if query["trim"][0] == "false":
                    trim = False
            gfm.generate(text=query["message"][0], out="final.png", trim=trim)
            self.send_response(200)
            self.send_header('content-type', 'image/png')
            self.end_headers()
            with open('final.png', 'rb') as final:
                for chunk in read_in_chunks(final, 512):
                    self.wfile.write(chunk)
            os.remove('final.png')
            

socketserver.TCPServer.allow_reuse_address = True

with socketserver.TCPServer(("", port), GraffitiHandler) as server:
    print('Serving at port %s' % port)
    server.serve_forever()
