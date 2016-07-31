import threading
import webbrowser
from wsgiref.simple_server import make_server
import math
import time

FILE = 'frontend.html'
PORT = 8080

fib_memo = {0: 0, 1: 1}

def fib(n):
    if n not in fib_memo:
        fib_memo[n] = fib(n-1) + fib(n-2)
    return fib_memo[n]
#    if n < 2:
#        return n
#    return fib(n-2) + fib(n-1)

def test_app(environ, start_response):
    if environ['REQUEST_METHOD'] == 'POST':
        try:
            request_body_size = int(environ['CONTENT_LENGTH'])
            request_body = environ['wsgi.input'].read(request_body_size)
        except (TypeError, ValueError):
            request_body = "0"
        try:
            start = time.time()
            result = fib(int(request_body))
            delta = time.time() - start
            response_body = '%d  (took %.6fs)' % (result, delta)
        except:
            response_body = "error"
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]
        start_response(status, headers)
        return [response_body]
    else:
        response_body = open(FILE).read()
        status = '200 OK'
        headers = [('Content-type', 'text/html'),
                   ('Content-Length', str(len(response_body)))]
        start_response(status, headers)
        return [response_body]

def open_browser():
    """Start a browser after waiting for half a second."""
    def _open_browser():
        webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))
    thread = threading.Timer(0.5, _open_browser)
    thread.start()

def start_server():
    """Start the server."""
    httpd = make_server("", PORT, test_app)
    httpd.serve_forever()

if __name__ == "__main__":
    open_browser()
    start_server()
