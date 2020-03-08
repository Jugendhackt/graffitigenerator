import http.server
import socketserver

port = 80
handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", port), handler) as server:
    print('Serving at port %s' % port)
    server.serve_forever()