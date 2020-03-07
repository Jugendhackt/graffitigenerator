const http = require('http');
const exec = require('child_process').exec;
const { parse } = require('querystring');
const fs = require('fs');
const port = 80;

http.createServer((req, res) => {
    var url = req.url;
    url = url.split('?')[0];
    var query;
    if (req.url.split('?').length > 1) {
        query = parse(req.url.split('?')[1]);
    }
    if (url = '/text') {
        if (query === undefined || query.message === undefined) {
            res.writeHead(404, 'Invalid message');
            res.end();
            return;
        }
        exec(`python3 textTransform.py ${query.message}`, (err) => {
            if (err) {
                res.writeHead(500, 'Internal Error');
                res.end();
                console.log(err);
                return;
            }
            
            try {
                res.writeHead(200, { 'content-type': 'image/png' });
                var s = fs.readFileSync('final.png');
                s.pipe(res);
                res.end();
            } catch (e) {
                console.log(e);
                res.writeHead(500, 'Internal Error');
                res.end();
            }
        });
    }
}).listen(port);
console.log('Listening on ' + port);