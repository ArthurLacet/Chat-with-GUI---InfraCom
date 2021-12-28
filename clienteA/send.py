import socket
import threading
from time import sleep

from PIL.Image import ENCODERS
from gui import gui

CLIENT_A_SENDER_ADDR = ('0.0.0.0', 12126)
CLIENT_B_SENDER_ADDR = ('0.0.0.0', 13136)

CLIENT_A_RECEIVER_ADDR = ('localhost', 14146)
CLIENT_B_RECEIVER_ADDR = ('localhost', 15156)

class sender:
    def __init__(self):
        self.setupSockets()
        print("sockets are ready")


        self.threadGUI = threading.Thread(target=self.interfaceThread, daemon=True)
        self.threadGUI.start()
        sleep(3)
        print("Começando Main Loop")
        self.mainLoop()

    def setupSockets(self):
        self.socket = socket.socket(type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self.socket.bind(CLIENT_A_SENDER_ADDR)
        self.socket.connect(CLIENT_B_RECEIVER_ADDR)
        print(f"connected with client B on IP {CLIENT_B_RECEIVER_ADDR[0]} on port {CLIENT_B_RECEIVER_ADDR[1]}")

    def interfaceThread(self):
        self.gui = gui.Gui()
        self.gui.run()
        print("Gui is ready")

    def mainLoop(self):
        while True:
            try:
                if len(self.gui.msgBuffer) != 0:
                    category, msg = self.gui.msgBuffer.pop(0)
                    if category == 0:  #enviar texto padrão
                        self.socket.sendall(bytes(msg,encoding="utf-8"))

                    elif category == 1: #enviar file
                        self.socket.send(bytes(f'º{msg[-4:]}','utf-8'))
                        self.fileLoop(msg)
            except Exception as e:
                print("deu merda,", e)
                break


    def fileLoop(self, filePath):
        with open(filePath,'rb') as file:
            chunck = file.read(1024)
            while chunck:
                self.socket.send(chunck)
                chunck = file.read(1024)
        self.socket.send(b'end')
        print("Trato Feito")
        print(self.socket.recv(1024))         

if __name__ == '__main__':
    try:
        client = sender()
    except Exception as e:
        input(e)