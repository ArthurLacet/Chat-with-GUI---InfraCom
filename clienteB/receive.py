import socket
import os

CLIENT_A_SENDER_ADDR = ('0.0.0.0', 12126)
CLIENT_B_SENDER_ADDR = ('0.0.0.0', 13136)

CLIENT_A_RECEIVER_ADDR = ('localhost', 14146)
CLIENT_B_RECEIVER_ADDR = ('localhost', 15156)


SCRIPT_DIR = os.path.dirname(__file__)
REL_PATH = r"inbox\text_messages.txt"
ABS_FILE_PATH = os.path.join(SCRIPT_DIR, REL_PATH)

class receiver:
    def __init__(self):
        self.setupSockets()
        print("sockets are ready")
        print("Iniciando Mainloop")
        self.mainLoop()
        self.t = 0


    def setupSockets(self):
        self.socket = socket.socket(type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(CLIENT_B_RECEIVER_ADDR)
        print(f"Client B receiver created at {CLIENT_B_RECEIVER_ADDR}")

        self.socket.listen(1)
        self.con, self.addr = self.socket.accept()
        print(f"Client B receiver connected with {self.addr}")

        
    def mainLoop(self):
        while True:
            try:
                msg = self.con.recv(1024)
                msg = msg.decode('utf-8')
                print("Client B received", msg)
                
                if msg[0] == 'º': # É arquivo
                    ext = msg[1:]
                    print("Receiving a file with extension: ", ext)
                    self.fileLoop(ext)
                
                else:
                    with open(ABS_FILE_PATH, 'a') as file:
                        file.write(msg + '\n')

            except Exception as e:
                print("Deu merda po, corrige isso dai", e)
                self.con.close()
                break

    def fileLoop(self, ext):
        print("começando fileloop")
        with open(f'inbox\PeloAmorDeDeusFunciona{ext}','wb') as file:
            while True:
                chunck = self.con.recv(1024)
                if chunck == b"end":
                    print("Trato Feito")
                    break
                file.write(chunck)
        self.con.send(b"Valeu mano, chegou aqui")  


if __name__ == "__main__": 
    server = receiver()