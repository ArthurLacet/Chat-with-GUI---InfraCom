import socket
import threading
from time import sleep
from datetime import datetime

from PIL.Image import ENCODERS
from gui import gui

CLIENT_A_SENDER_ADDR = ('0.0.0.0', 12122)
CLIENT_B_SENDER_ADDR = ('0.0.0.0', 13132)

CLIENT_A_RECEIVER_ADDR = ('localhost', 14142)
CLIENT_B_RECEIVER_ADDR = ('localhost', 15152)

class sender:
    def __init__(self):
        self.setupSockets()
        print("Sockets are:     Ready")
        print("MainLoop is:     Initializing")
        self.threadMainLoop = threading.Thread(target=self.mainLoop, daemon=True)
        self.threadMainLoop.start()
        print("MainLoop is:     Running")
        print("GUI      is:     Initializing")
        self.interface()

    def setupSockets(self):
        self.socket = socket.socket(type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(CLIENT_B_SENDER_ADDR)
        self.socket.connect(CLIENT_A_RECEIVER_ADDR)
        print(f"connected with client A on IP {CLIENT_A_RECEIVER_ADDR[0]} on port {CLIENT_A_RECEIVER_ADDR[1]}")

    def interface(self):
        print("GUI      is:     Running")
        self.gui = gui.Gui()
        self.gui.run()
        

    def mainLoop(self):
        sleep(0.5)
        print("Ready to send messages")
        while True:
            try:
                if self.gui.quit:
                    self.socket.sendall(bytes("ªquit",encoding="utf-8"))
                    quit()

                if len(self.gui.msgBuffer) != 0:
                    category, msg = self.gui.msgBuffer.pop(0)
                    if category == 0:  #enviar texto padrão
                        relogioQhorasSao = datetime.now()
                        sao = relogioQhorasSao.strftime("%H:%M")
                        msg = f'[{sao}]: {msg}'
                        self.socket.sendall(bytes(msg,encoding="utf-8"))

                    elif category == 1: #enviar file
                        self.socket.send(bytes(f'º{msg[-4:]}','utf-8'))
                        self.fileLoop(msg)
            except Exception as e:
                print("deu ruim,", e)
                break


    def fileLoop(self, filePath):
        with open(filePath,'rb') as file:
            chunck = file.read(1024)
            while chunck:
                self.socket.send(chunck)
                chunck = file.read(1024)
        self.socket.send(bytes('end','utf-8'))
        print("File Status:     Sent")
        print('Message from receiver:   ',self.socket.recv(1024).decode('utf-8'))                 

if __name__ == '__main__':
    try:
        client = sender()
    except Exception as e:
        input(e)