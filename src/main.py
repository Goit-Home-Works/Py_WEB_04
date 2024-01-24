import json
import datetime
import logging
import pathlib
import socket
from urllib.parse import parse_qs, urlparse, unquote_plus
import mimetypes
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
import pathlib

from jinja2 import Environment, FileSystemLoader

BASE_DIR = pathlib.Path()
data_file_path = BASE_DIR.joinpath('storage/data.json')
env = Environment(loader=FileSystemLoader('templates'))
SERVER_IP = '127.0.0.1'
SERVER_PORT = 5005
BUFFER = 1024


def send_data_to_socket(body):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.sendto(body, (SERVER_IP, SERVER_PORT))
    client_socket.close()


class HTTPHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length).decode('utf-8')
        params = parse_qs(body)
        current_datetime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_object = {key: value[0] for key, value in params.items()}
        new_object['current_datetime'] = current_datetime
        print(new_object)
        data_file_path = BASE_DIR.joinpath('storage/data.json')
        
        with open(data_file_path, 'r', encoding='utf-8') as existing_file:
            try:
                existing_data = json.load(existing_file)
            except json.decoder.JSONDecodeError:
                existing_data = []

        existing_data.append(new_object)

        with open(data_file_path, 'w', encoding='utf-8') as updated_file:
            json.dump(existing_data, updated_file, ensure_ascii=False, indent=2)
            updated_file.write('\n') 
        
        self.send_response(302)
        self.send_header('Location', './blog')
        self.end_headers()
           

    def do_GET(self):
        route = urlparse(self.path)
        match route.path:
            case "/":
                self.send_html('index.html')
            case "/message":
                self.send_html('message.html')
            case "/blog":
                self.render_template('blog.html')
            case _:
                file = BASE_DIR / route.path[1:]
                if file.exists():
                    self.send_static(file)
                else:
                    self.send_html('error.html', 404)

    def send_html(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())

    def render_template(self, filename, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open('storage/data.json', 'r', encoding='utf-8') as fd:
            r = json.load(fd)
        template = env.get_template(filename)
        print(template)
        html = template.render(blogs=r)
        self.wfile.write(html.encode())

    def send_static(self, filename):
        self.send_response(200)
        mime_type, *rest = mimetypes.guess_type(filename)
        if mime_type:
            self.send_header('Content-Type', mime_type)
        else:
            self.send_header('Content-Type', 'text/plain')
        self.end_headers()
        with open(filename, 'rb') as f:
            self.wfile.write(f.read())


def run(server=HTTPServer, handler=HTTPHandler):
    address = ('0.0.0.0', 3005)
    http_server = server(address, handler)
    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()


def save_data(data):
    body = unquote_plus(data.decode())
    try:
        payload = {key: value for key, value in [el.split('=') for el in body.split('&')]}
        with open(BASE_DIR.joinpath('storage/data.json'), 'w', encoding='utf-8') as fd:
            json.dump(payload, fd, ensure_ascii=False)
    except ValueError as err:
        logging.error(f"Field parse data {body} with error {err}")
    except OSError as err:
        logging.error(f"Field write data {body} with error {err}")


def run_socket_server(ip, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server = ip, port
    server_socket.bind(server)
    try:
        while True:
            data, address = server_socket.recvfrom(BUFFER)
            save_data(data)
    except KeyboardInterrupt:
        logging.info('Socket server stopped')
    finally:
        server_socket.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(threadName)s %(message)s")
    STORAGE_DIR = pathlib.Path().joinpath('storage')
    FILE_STORAGE = STORAGE_DIR / 'data.json'
    if not FILE_STORAGE.exists():
        with open(FILE_STORAGE, 'w', encoding='utf-8') as fd:
            json.dump({}, fd, ensure_ascii=False)

    thread_server = Thread(target=run)
    thread_server.start()
    thread_socket = Thread(target=run_socket_server(SERVER_IP, SERVER_PORT))
    thread_socket.start()
