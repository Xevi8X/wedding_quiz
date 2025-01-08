from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        assert hasattr(server, 'status')
        assert hasattr(server, 'config')
        
    def get_root(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=UTF-8')
        self.end_headers()
        with open(self.server.config['root_html'], 'r', encoding='utf-8') as file:
            self.wfile.write(file.read().encode('utf-8'))

    def get_state(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=UTF-8')
        self.end_headers()
        self.wfile.write(self.server.status.as_json().encode('utf-8'))

    def not_found(self):
        self.send_response(404)
        self.send_header('Content-type', 'text/plain; charset=UTF-8')
        self.end_headers()
        self.wfile.write('Not Found'.encode('utf-8'))
    
    def do_GET(self):
        get_routes = {
            '/': self.get_root,
            '/index.html': self.get_root,
            '/state': self.get_state
        }
        try:
            get_routes[self.path]()
        except Exception as e:
            print(e)
            self.not_found()

class RestServer (HTTPServer):
    def __init__(self, ip, port, status, config):
        self.status = status
        self.config = config
        super().__init__((ip, port), RequestHandler)

    def start(self):
        http_thread = threading.Thread(target=self.serve_forever)
        http_thread.daemon = True
        http_thread.start()

if __name__ == '__main__':
    class MockStatus:
        def as_json(self):
            with open('examples/quiz_content.json', 'r', encoding='utf-8') as file:
                return file.read()
        
    mock_config = {
        'root_html': 'assets/index.html'
    }

    server = RestServer('', 1234, MockStatus(), mock_config)
    server.start()

    while True:
        time.sleep(1)
        print('Server is running...')

    
