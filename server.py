#  coding: utf-8 
import socketserver
from pathlib import Path

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
        resp = 'HTTP/1.1 ' + self.invoke_method() + '\r\n'
        self.request.sendall(bytearray(resp,'utf-8'))


    def parse_request(self):
        req = self.data.splitlines()
        req_line = req[0]
        # Figure out where the headers end and the body begins, save the body,
        # then remove it from the list.
        if b'' in req:
            headers_end = req.index(b'')
            if headers_end+1 < len(req):
                req_body = req[headers_end+1 : ]    # TODO make it self.req_body
            del req[headers_end:]
        # TODO: if the split below fails, raise a BadRequestLineError or
        # something. May need to look into request's HTTPError or something;
        # it seems the tests might expect it. But be careful, do you really want
        # your server to crash because of a bad request or something?
        #try:
        self.method, self.uri, self.version = req_line.split(None, 2)
        #except ValueError as e:
        #    raise Exception()
        req_headers = req[1:]
        for i in range(len(req_headers)):
            req_headers[i] = req_headers[i].split()
        self.headers = dict(req_headers)


    def invoke_method(self):
        # TODO: Add checks for self.version, make sure it matches HTTP/1.1 or
        # whatever else we want to allow.
        if self.method == b'GET':
            return self.get()
        # elif self.method == b'POST':
        #     pass
        # elif self.method == b'HEAD':
        #     pass
        # elif self.method == b'PUT':
        #     pass
        # elif self.method == b'DELETE':
        #     pass
        # elif self.method == b'PATCH':
        #     pass
        # elif self.method == b'OPTIONS':
        #     pass
        # elif self.method == b'TRACE':
        #     pass
        # elif self.method == b'CONNECT':
        #     pass
        else:
            return '405 Method Not Allowed\r\n'

    
    def get(self):
        """
        From https://www.rfc-editor.org/rfc/rfc2616#section-9.3
        The GET method means retrieve whatever information (in the form of an
        entity) is identified by the Request-URI. If the Request-URI refers
        to a data-producing process, it is the produced data which shall be
        returned as the entity in the response and not the source text of the
        process, unless that text happens to be the output of the process.
        """

        # Path stuff
        uri = Path(self.uri.decode())
        www = Path('./www').resolve()
        index = Path('index.html')
        uri = www / uri.resolve().relative_to('/')

        # Status Line Strings
        full_addr = f'''http://{self.server.server_address[0]}:{
                                        self.server.server_address[1]}{
                                                           self.uri.decode()}'''
        code_404 = f'404 {full_addr} Not Found \r\n'
        code_301 = f'301 Moved\r\nLocation: {full_addr}/\r\n'
        code_200 = '200 OK\r\n\r\n{body}\r\n'

        # Check if it exists and all that
        if not uri.exists():
            # If the uri does not exist
            return code_404
        elif not uri.is_dir():
            # If the uri exists and is not a directory
            return code_200.format(body=uri.read_text())
        elif self.uri[-1:] != b'/':
            # If the uri is an existing directory, but does not end with '/'
            return code_301
        elif not (uri / index).exists():
            # If the uri is an existing directory, but does not have a file
            # called index.html
            return code_404
        else:
            # If the uri is an existing directory and has index.html inside it.
            return code_200.format(body=(uri / index).read_text())


    # def post(self):
    #     # 405 Method Not Allowed
    #     pass
    # def head(self):
    #     # 405
    #     pass
    # def put(self):
    #     # 405
    #     pass
    # def delete(self):
    #     # 405
    #     pass
    # def patch(self):
    #     # 405
    #     pass
    # def options(self):
    #     # 405
    #     pass
    # def trace(self):
    #     # 405
    #     pass
    # def connect(self):
    #     # 405
    #     pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
