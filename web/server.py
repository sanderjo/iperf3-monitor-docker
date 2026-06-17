#!/usr/bin/env python3
import http.server
import json
import os

RESULTS_FILE = '/data/results.jsonl'
WEB_DIR = '/web'


class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/api/results':
            self.serve_results()
        elif self.path in ('/', '/index.html'):
            self.serve_file('index.html', 'text/html; charset=utf-8')
        else:
            self.send_error(404)

    def serve_results(self):
        results = []
        try:
            with open(RESULTS_FILE) as f:
                for line in f:
                    line = line.strip()
                    if line:
                        results.append(json.loads(line))
        except FileNotFoundError:
            pass

        body = json.dumps(results[-500:]).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, name, content_type):
        path = os.path.join(WEB_DIR, name)
        try:
            with open(path, 'rb') as f:
                body = f.read()
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(body))
            self.end_headers()
            self.wfile.write(body)
        except FileNotFoundError:
            self.send_error(404)

    def log_message(self, fmt, *args):
        pass


if __name__ == '__main__':
    addr = ('0.0.0.0', 8080)
    httpd = http.server.HTTPServer(addr, Handler)
    print(f"Web UI available at http://localhost:8080")
    httpd.serve_forever()
