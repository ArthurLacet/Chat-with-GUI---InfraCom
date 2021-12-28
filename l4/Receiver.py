import socket
import os

CLIENT_SENDER_ADDR = ('0.0.0.0', 12124)
CLIENT_RECEIVER_ADDR = ('localhost', 15154)

SCRIPT_DIR = os.path.dirname(__file__)
REL_PATH = r"text_messages_log.txt"
ABS_FILE_PATH = os.path.join(SCRIPT_DIR, REL_PATH)
ABS_FILE_PATH_FILES = SCRIPT_DIR

class receiver:
    def __init__(self):
        self.t = 0
        self.setupSockets()
        print("Sockets are:     Ready")
        print("MainLoop is:     Initializing")
        self.mainLoop()


    def setupSockets(self):
        self.socket = socket.socket(type=socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(CLIENT_RECEIVER_ADDR)
        print(f"Client B receiver created at {CLIENT_RECEIVER_ADDR}")

        self.socket.listen(1)
        self.con, self.addr = self.socket.accept()
        print(f"Client B receiver connected with {self.addr}")

        
    def mainLoop(self):
        while True:
            try:
                msg = self.con.recv(1024)
                msg = msg.decode('utf-8')
                print("Client B received", msg)
                if msg == 'ªend':
                    self.con.close()
                    print("Conexion is:     Closed")
                    quit()

                if msg[0] == 'º': # É arquivo
                    ext = msg[1:]
                    if msg[1:] == 'jpeg': 
                        msg = '.jpeg'
                        ext = msg                        
                    print(f"Receiving a file with extension:    {ext}")
                    self.fileLoop(ext)
                
                else:
                    with open(ABS_FILE_PATH, 'a') as file:
                        file.write(msg + '\n')

            except Exception as e:
                print("Deu ruim, corrige isso dai: ", e)
                self.con.close()
                break

    def fileLoop(self, ext):
        print("File loop:       Running")
        with open(f'{ABS_FILE_PATH_FILES}\File{("0" if self.t < 10 else "")}{self.t}{ext}','wb') as file:
            chunck = self.con.recv(1024)               
            while chunck:
                if chunck == bytes('end','utf-8') or chunck[-3:] == bytes('end','utf-8'):
                    print("File Status:     Arrived")
                    break
                file.write(chunck)
                chunck = self.con.recv(1024)
        self.con.send(b"File received") 
        self.t += 1  


if __name__ == "__main__": 
    server = receiver()