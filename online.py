__author__ = 'Андрей'
from socket import socket,AF_INET,SOCK_STREAM
import re
import pickle

class Host:
    def __init__(self,port=1994,portionSize=1024,maxContacts=1):
        self.port=port
        self.maxContacts=maxContacts
        self.portionSize=portionSize
        self.sock=socket(AF_INET, SOCK_STREAM)
        self.error = None

    def start(self,host=''):
        self.sock.bind(('',self.port))
        self.sock.listen(self.maxContacts)
        self.connection, self.address = self.sock.accept()
        #self.connection.settimeout(5)

    def getData(self):
        try:
            while True:
                data = self.connection.recv(self.portionSize)
                if data is None:
                    break
                return data
        except:
            self.error="get data error"
        finally:
            self.close()

    def sendData(self,data):
        try:
            self.connection.send(data)
            return data
        except:
            self.error="send data error"
        finally:
            self.close()

    def sendPickle(self,data):
        return self.sendData(pickle.dumps(data))

    def getPickle(self):
        return pickle.loads(self.getData())

    def close(self):
        self.sock.close()

class Client:
    def __init__(self,port=1994,portionSize=1024):
        self.port=port
        self.portionSize=portionSize
        self.sock=socket(AF_INET, SOCK_STREAM)
        self.error=None

    def start(self,ip="localhost"):
        self.sock.connect((ip, self.port))

    def getData(self):
        try:
            while True:
                data = self.sock.recv(self.portionSize)
                if not data:
                    break
                return data
        except:
            self.error="get data error"

    def sendData (self,data):
        try:
            self.sock.send(data)
            return data
        except:
            self.error="send data error"

    def sendPickle(self,data):
        return self.sendData(pickle.dumps(data))

    def getPickle(self):
        return pickle.loads(self.getData())


ipReg=re.compile('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')


def isItIp(ip):
    if ipReg.match(ip) is None:
        return False

    parts = ip.split(".")

    if len(parts)!=4:
        return False

    if int(parts[0])==0 or (parts[3])==0:
        return False

    for part in parts:
        if (255 < int(part) < 0) or ( len(part) > 4):
            return False

    return True

if __name__ == "__main__":
    pass