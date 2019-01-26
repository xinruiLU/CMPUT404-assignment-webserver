#  coding: utf-8
import socketserver
import os

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

    def handle(self):
        #decode find from
        #https://stackoverflow.com/questions/606191/convert-bytes-to-a-string
        #Aaron Maenpaa
        self.data = self.request.recv(1024).strip().decode('utf-8')
        print ("Got a request of: %s\n" % self.data)
        the_file = self.data.split()[1]
        the_request = self.data.split()[0]
        #self.request.sendall(bytearray("OK",'utf-8'))
        #get absolute path of the current file find from
        #https://blog.csdn.net/lom9357bye/article/details/79285170
        # S_H-A_N
        current_fpath = os.path.abspath(__file__)
        #print(current_fpath)
        #get current path name find from
        #https://blog.csdn.net/longshenlmj/article/details/13294871
        # willard
        name_fpath = os.path.dirname(current_fpath)
        path = name_fpath+"/www"+the_file
        #print (path)

        if (os.path.abspath(path)):
            if  not "/www" in path:
                self.send_404(self.request)
                return
        else:
            self.send_404(self.request)
            return


        if the_request=="GET":
            #check if path is a file or is a directory find from
            #https://blog.csdn.net/StephenHendery/article/details/79049521
            # stephenhendery

            # looked at
            #https://github.com/sjpartri/cmput404assignments/blob/master/CMPUT404-assignment-webserver-master/server.py
            #Sean Partridge sjpartri

            #https://github.com/sam9116/cmput404-assignment1/blob/master/server.py
            #Sam Bao sam9116

            if os.path.isfile(path):
                get_type = path.split(".")[-1]
                if(get_type == "css" or get_type == "html"):
                    get_type = "text/"+get_type
                    self.send_200_OK(self.request,path,name_fpath,get_type)
                else:
                    self.send_404(self.request)
            elif os.path.isdir(path):
                if the_file.endswith("/"):
                    path = path + "index.html"
                else:
                    path = path + "/index.html"
                if os.path.isfile(path):
                    get_type = "text/html\n\n"
                    self.send_200_OK(self.request,path,name_fpath,get_type)
            else:
                self.send_404(self.request)
        else:
            self.send_405(self.request)
    def send_404(self,request):
        self.request.sendall(bytearray("HTTP/1.1 404 Not Found \r\n",'utf-8'))
        return

    def send_200_OK(self,request,path,name_fpath,get_type):
        #looked at
        #https://stackoverflow.com/questions/27206838/how-to-finish-a-socket-file-transfer-in-python
        #Leandro
        open_file = open(path)

        self.request.sendall(bytearray("HTTP/1.1 200 OK \r\nContent-Type: "+ get_type+
        ";Transfer-Encoding: chunked;\r\n\r\n"+open_file.read(1024),'utf-8'))
        open_file.close()
        return

    def send_405(self,request):
        self.request.sendall(bytearray("HTTP/1.1 405 Method Not Allowed \r\n",'utf-8'))



if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
