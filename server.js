const http = require('http');
const { spawn } = require('child_process');
const { parse } = require('querystring');
const fs = require('fs');
const port = 80;
const illegal = [];

var server = http.createServer((req, res) => {
    var url = req.url;
    url = url.split('?')[0];
    var query;
    if (req.url.split('?').length > 1) {
        query = parse(req.url.split('?')[1]);
    }
    if (url == '/text') {
        if (query === undefined || query.message === undefined) {
            res.writeHead(400, 'Invalid message');
            res.end();
            return;
        }
        console.log('Got text request: ' + query.message);
        var proc = spawn('python3', ['textTransform.py']);
        var pstdin = proc.stdin;
        pstdin.setEncoding('utf-8');
        pstdin.write(query.message + '\n');
        pstdin.end();

        proc.on('close', (code) => {
            try {
                var s = fs.createReadStream('final.png');
                res.writeHead(200, { 'content-type': 'image/png' });
                s.pipe(res)
                .on('finish', () => {
                    res.end();
                });
            } catch (e) {
                res.writeHead(500, 'Internal Error');
                console.log(e);
                res.end();
            }
        });
    } else if (url == '/test'){
        res.writeHead(200, { 'content-type': 'text/plain' });
        res.end('hi');
    }
}).listen(port);
server.timeout = 120000;
console.log('Listening on ' + port);