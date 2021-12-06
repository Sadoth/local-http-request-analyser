#!/usr/bin/python 
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler


class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = f"<html><body><h1>{message}</h1></body></html>"
        return content.encode("utf8")  # NOTE: must return a bytes object!
    
    def print_request(self, method):
        print("\n\n------------------------------------------------------------------")
        print("Method : "+ method)
        print("Path : " + self.path)
        print("headers : [")
        for header in self.headers:
            print("\t"+str(header)+" : "+ str(self.headers.get(header)))
        print("]")
        content_len = 0
        if self.headers.get('Content-Length'):
            content_len = int(self.headers.get('Content-Length'))
        if content_len == 0 :
            print("No body")
        else :
            print(self.rfile.read(content_len))

    def do_GET(self):
        self.print_request("GET")
        self._set_headers()
        self.wfile.write(self._html("GET!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self.print_request("POST")
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))
        
    def log_message(self, format, *args):
        return

def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
    server_address = (addr, port)
    httpd = server_class(server_address, handler_class)

    print(f"Starting httpd server on {addr}:{port}")
    httpd.serve_forever()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Run a simple HTTP server")
    parser.add_argument(
        "-l",
        "--listen",
        default="localhost",
        help="Specify the IP address on which the server listens",
    )
    parser.add_argument(
        "-p",
        "--port",
        type=int,
        default=8000,
        help="Specify the port on which the server listens",
    )

    args = parser.parse_args()
    
    run(addr=args.listen, port=args.port)
