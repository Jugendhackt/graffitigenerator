const http = require('http');
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
        if (query.message === undefined) {
            res.writeHead(404, 'Invalid message');
            return;
        }
        
    }
});