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

        while True:
            response = self.clientsocket.recv(2048).decode(encoding='utf_8', errors='strict')

            if response != "":
                self.execute(response)
            else:
                print ("No response received.")

            print("Client déconnecté...")

    def execute(self, response):
        response = response.strip()

        args = response.split(",")

        action = args[0]

        del args[0]

        print ("Action: " + str(action))
        print ("Args: " + str(args))

        if action == CMD_FWD:
            msg = "Executing action: " + str(action) + "..."
            print(msg)
            self.send(msg)
            th = threading.Thread(target=self.pipo.forward, args=args)
            th.daemon = True
            th.start()
        elif action == CMD_BWD:
            msg = "Executing action: " + str(action) + "..."
            print(msg)
            self.send(msg)
            th = threading.Thread(target=self.pipo.backward, args=args)
            th.daemon = True
            th.start()
        elif action == CMD_LEFT:
            msg = "Executing action: " + str(action) + "..."
            print(msg)
            self.send(msg)
            th = threading.Thread(target=self.pipo.left, args=())
            th.daemon = True
            th.start()
        elif action == CMD_RIGHT:
            msg = "Executing action: " + str(action) + "..."
            print(msg)
            self.send(msg)
            fw = threading.Thread(target=self.pipo.right, args=())
            fw.daemon = True
            fw.start()
        elif action == CMD_STOP:
            msg = "Executing action: " + str(action) + "..."
            print(msg)
            self.send(msg)
            th = threading.Thread(target=self.pipo.stop, args=())
            th.daemon = True
            th.start()
        else:
            msg = "command not found !"
            print(msg)
            self.send(msg)

    def send(self, msg):
        self.clientsocket.send(msg.encode(encoding='utf_8', errors='strict'))


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind(("", PORT))

while True:
    tcpsock.listen(1)
    print("En écoute...")
    (clientsocket, (ip, port)) = tcpsock.accept()
    newthread = ClientThread(ip, port, clientsocket)
    newthread.start()