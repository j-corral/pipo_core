#!/usr/bin/env python
# coding: utf-8

import Pipo
import socket
import threading

PORT = 9696

M_CONF = [
    {
        "name": "M1",
        "pins":[36, 38, 40],
        "pwm_pin": 40,
        "forward":[1, 0, 1],
        "backward":[0, 1, 1],
    },
    {
        "name": "M2",
        "pins":[19, 21, 23],
        "pwm_pin": 19,
        "forward":[1, 0, 1],
        "backward":[1, 1, 0]
    },
    {
        "name": "M3",
        "pins":[11, 13, 15],
        "pwm_pin": 11,
        "forward":[1, 1, 0],
        "backward":[1, 0, 1]
    },
    {
        "name": "M4",
        "pins":[22, 24, 26],
        "pwm_pin": 26,
        "forward":[0, 1, 1],
        "backward":[1, 0, 1]
    }

]

S_CONF = {
    "pin_sig": 33,
    "pin_trig": 31,
    "pin_echo": 29
}


CMD_FWD = "forward"
CMD_BWD = "backward"
CMD_STOP = "stop"
CMD_LEFT = "left"
CMD_RIGHT = "right"

class ClientThread(threading.Thread):

    def __init__(self, ip, port, clientsocket):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.clientsocket = clientsocket
        self.pipo = Pipo.Pipo(M_CONF, S_CONF)
        print("[+] Nouveau thread pour %s %s" % (self.ip, self.port,))

    def run(self):
        print("Connection de %s %s" % (self.ip, self.port,))

        response = self.clientsocket.recv(2048)

        if response != "":
            self.execute(response)

        print("Client déconnecté...")

    def execute(self, response):
        response = response.strip()
        print ("Received: " + response)

        if response == CMD_FWD:
            msg = "Executing forward..."
            print(msg)
            self.clientsocket.send(msg)
            self.pipo.forward()
        elif response == CMD_BWD:
            msg = "Executing backward..."
            print(msg)
            self.clientsocket.send(msg)
            self.pipo.backward()
        elif response == CMD_LEFT:
            msg = "Executing left..."
            print(msg)
            self.clientsocket.send(msg)
            self.pipo.left()
        elif response == CMD_RIGHT:
            msg = "Executing right..."
            print(msg)
            self.clientsocket.send(msg)
            self.pipo.right()
        elif response == CMD_STOP:
            msg = "Executing stop..."
            print(msg)
            self.clientsocket.send(msg)
            self.pipo.stop()
        else:
            msg = "command not found !"
            print(msg)
            self.clientsocket.send(msg)


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", PORT))

while True:
    tcpsock.listen(10)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()