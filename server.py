#  coding: utf-8 
import socketserver

# Copyright 2013 Abram Hindle, Eddie Antonio Santos, Sean Meyers
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        self.parse_request()
        self.invoke_method()
        self.request.sendall(bytearray("OK",'utf-8'))

    def parse_request(self):
        req = self.data.splitlines()
        req_line = req[0]
        # TODO: if the split below fails, raise a BadRequestLineError or something. May need to look into request's HTTPError or something; it seems the tests might expect it.
        #try:
        self.method, self.uri, self.version = req_line.split(None, 2)
        #except ValueError as e:
        #    raise Exception()
        message = req[1:]
        for i in range(len(message)):
            message[i] = message[i].split()
        self.headers = dict(message)

    def invoke_method(self):
        if self.method == b'GET':
            pass
        elif self.method == b'POST':
            pass
        elif self.method == b'HEAD':
            pass
        elif self.method == b'PUT':
            pass
        elif self.method == b'DELETE':
            pass
        elif self.method == b'PATCH':
            pass
        elif self.method == b'OPTIONS':
            pass
        elif self.method == b'TRACE':
            pass
        elif self.method == b'CONNECT':
            pass
        else:
            # TODO: raise InvalidHTTPMethodError
            pass

    # TODO: Implement methods. Can start with sending back 501 Not Implemented s
    def get(self):
        pass
    def post(self):
        pass
    def head(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass
    def patch(self):
        pass
    def options(self):
        pass
    def trace(self):
        pass
    def connect(self):
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
