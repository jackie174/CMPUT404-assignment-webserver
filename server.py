#  coding: utf-8 
import socketserver
import os
import time
# Copyright 2013 Abram Hindle, Eddie Antonio Santos
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
    root = "./www"
    def statu_200(self,content_type, content_len, file):
        current_time = time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
        send = f"HTTP/1.1 200 OK\r\nDate: {current_time}\r\nContent-Type: {content_type}\r\nContent-Length: {content_len}\r\n\r\n{file}"
        self.request.sendall(bytearray(send, "utf-8"))
    def statu_301(self, location=None):
        current_time = time.strftime("%a, %d %b %Y %I:%M:%S %Z", time.gmtime())
        send = f"HTTP/1.1 301 Moved Permanently\r\nDate: {current_time}\r\n\r\nLocation: {location}"
        self.request.sendall(bytearray(send, "utf-8"))
    def statu_404(self):
        send = "HTTP/1.1 404 Not Found\r\n"
        self.request.sendall(bytearray(send, "utf-8"))
    def statu_405(self):
        send = "HTTP/1.1 405 Method Not Allowed\r\n"
        self.request.sendall(bytearray(send, "utf-8"))


    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)
        data_decode= self.data.decode("utf-8").split("\r\n")
        header_string = data_decode[0]
        print(header_string)
        try:
            method, path, HTTP_version = header_string.split(" ")
        except:
            self.statu_404()
        #without this line, we cannnot see the 404 error in the website page.
        #if we want to get root.png / deep.png correctly, we need to comment this line
        #self.request.sendall(bytearray("     ", "utf-8"))
        path_abs = os.path.abspath(self.root+ path)

        if method != "GET":
            self.statu_405()

        else:
           
            if os.path.exists(path_abs) and (path.endswith("/") or "." in path):
                if ".css" in path_abs:
                    try:
                        f = open(path_abs, "r")
                        return_text = f.read()
                        self.statu_200("text/css", len(return_text), return_text)
                    except:
                        self.statu_404()
                    finally:
                        f.close()

                elif ".html" in path_abs:
                    try:
                        f = open(path_abs, "r")
                        return_text = f.read()
                        self.statu_200("text/html", len(return_text), return_text)
                    except:
                        self.statu_404()
                    finally:
                        f.close()

                else:
                    if path.endswith("/"):
                        path_abs = os.path.realpath(self.root+ path)
                        try:
                            f = open(path_abs+"/index.html", "r")
                            return_text = f.read()
                            self.statu_200("text/html", len(return_text), return_text)
                            
                        except:
                            self.statu_404()
                        finally:
                            f.close()
                    else:
                        self.statu_404()

            elif os.path.exists(path_abs) and not path.endswith("/"):
                print("--")
                path_abs = os.path.abspath(self.root+ path + "/")
                print(path_abs)
                try:
                    self.statu_301(path_abs)
                except:
                    self.statu_404()
            else:
                self.statu_404()    


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
