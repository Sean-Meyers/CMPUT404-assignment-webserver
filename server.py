#  coding: utf-8 
import socketserver
import os

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
        # TODO: if the split below fails, raise a BadRequestLineError or
        # something. May need to look into request's HTTPError or something;
        # it seems the tests might expect it.
        #try:
        self.method, self.uri, self.version = req_line.split(None, 2)
        #except ValueError as e:
        #    raise Exception()
        message = req[1:]
        for i in range(len(message)):
            message[i] = message[i].split()
        self.headers = dict(message)


    def invoke_method(self):
        # TODO: Add checks for self.version, make sure it matches HTTP/1.1 or
        # whatever else we want to allow.
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


    # TODO: Implement methods. Can start with sending back 501 Not Implementeds
    
    def get(self):
        """
        From https://www.rfc-editor.org/rfc/rfc2616#section-9.3
        The GET method means retrieve whatever information (in the form of an
        entity) is identified by the Request-URI. If the Request-URI refers
        to a data-producing process, it is the produced data which shall be
        returned as the entity in the response and not the source text of the
        process, unless that text happens to be the output of the process.
        """
        # 200 OK
        # 404
        # 301 (for deep)
        
        os.chdir('./www')
        # Split the uri into a list such that deeper directories have higher
        # indices in the list, then remove all b'' characters from the result.
        requested_thing = self.uri.split(b'/')
        for null in [thing for thing in requested_thing if thing == b'']:
            requested_thing.remove(null)
        requested_thing.reverse()   # So we can use pop conveniently

        if requested_thing.pop().decode() in os.listdir():
            # 200 OK, send them the thing, or chdir to the requested dir and repeat
            # Use the len(requested_thing) to determine if it's a file or directory the user wants
            pass
        else:
            # 404 Not Found Mate
            pass
        # get root from '/', idk what gets returned
        pass

    def post(self):
        # 405 Method Not Allowed
        pass

    def head(self):
        """
        From https://www.rfc-editor.org/rfc/rfc2616#section-9.4
        The HEAD method is identical to GET except that the server MUST NOT
        return a message-body in the response. The metainformation contained
        in the HTTP headers in response to a HEAD request SHOULD be identical
        to the information sent in response to a GET request. This method can
        be used for obtaining metainformation about the entity implied by the
        request without transferring the entity-body itself. This method is
        often used for testing hypertext links for validity, accessibility,
        and recent modification.
        """
        # 200 OK
        # 404 ?
        # 301 (for deep) ?
        pass

    def put(self):
        # 405
        pass

    def delete(self):
        # 405
        pass

    def patch(self):
        # 405 or 501 (Not Implemented)
        pass

    def options(self):
        # 405 or 501 (Not Implemented)
        pass

    def trace(self):
        # 405 or 501 (Not Implemented)
        pass

    def connect(self):
        # 405 or 501 (Not Implemented)
        pass


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
