from os import path
import tkinter
from tkinter import Scrollbar, font
from tkinter.constants import ANCHOR, BOTH, BOTTOM, CENTER, DISABLED, END, FLAT, RAISED, S, YES
from tkinter import filedialog
from types import TracebackType
from PIL import ImageTk, Image
import tkinter.scrolledtext
from datetime import date, datetime

import vlc

"""
* Deve existir uma rótulo com o nome do programa;
* Deve existir um campo para digitar a mensagem;
* Deve existir um botão de enviar, que pega a mensagem que foi digitada, envia ao destinatário e limpa o campo de digitação, para que o usuário possa digitar outra mensagem em seguida;
* Deve haver a possibilidade de enviar mensagens através da tecla “Enter”, funcionando de modo semelhante ao botão de enviar.
* Deve existir uma área em que as mensagens enviadas sejam visualizadas, e cada mensagem deve ser exibida com sua hora de envio;
* Não devem ser enviadas mensagens vazias nem mensagens em branco;
* Deve existir um botão que limpa o chat.
* Deve ser possível o envio de anexo através de um botão, onde será possível escolher um arquivo do computador do usuário e enviá-lo ao destinatário. Esse arquivo poderá ser um vídeo, foto ou música.
* Deve haver no chat a visualização do arquivo enviado. Por exemplo: exibir a miniatura da imagem ou a possibilidade de reproduzir o vídeo, ou música escolhida.  
"""

# Cores temas da GUI
BLUE = '#1f5563'
HBLUE = '#43b9d8'
LBLUE = '#1ca3c6'
RED = '#941f1f'

# Path das Profile Pics
MYPFP = r'C:\git-repositories\Infracom\lista 4\gui\me.png'
MYNICK = r'bot'
MYSTATUS = r'Online'
MYCUSTOMSTATUS = r'Fazendo nada'

FRIENDPFP = r'C:\git-repositories\Infracom\lista 4\gui\a.png'
FRIENDNICK = r'Cauê'
FRIENDSTATUS = r'Online'
FRIENDCUSTOMSTATUS = r'Fazendo nada'

IMAGEEXT = ['.jpg', '.jpeg', '.jpe', '.jif', '.jfif', '.jfi', '.png',
            '.webp', '.tiff', '.tif', '.psd', '.raw', '.arw', '.cr2', '.nrw', '.k25',
            '.svg', '.svgz', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2', '.bmp', '.dib',
            '.heif', '.heic', '.ind', '.indd', '.indt', '.jp2', '.j2k', '.jpf', '.jpx', '.jpm', '.mj2'
            ]

AUDIOEXT = ['.wv', '.wma', '.webm', '.wav', '.vox', '.voc', '.tta', 'sln', 'rf64', '.raw', '.ra', '.rm', '.opus', '.ogg', '.oga', '.mogg', '.nmf', '.msv', '.mpc', '.mp3', '.mmf',
            '.m4p', '.m4b', '.m4a', '.ivs', '.iklax', '.gsm', '.flac', '.dvf', '.dss', '.cda', '.awb', '.au', '.ape', '.alac', '.aiff', '.act', '.aax', '.aac', '.aa', '.8svx', '.3gp']

CURSOR = 'hand2'
class Gui():
    def __init__(self):
        #! Params
        _windowlenght = "800x600"
        _title = "Discord da DeepWeb"

        #! boolean variables
        self.isRunning = False

        #! Window Settings
        self.r = tkinter.Tk()
        self.r.title(_title)
        self.r.geometry(_windowlenght)
        self.r.resizable(False, False)

        self.setProfilesCfg()

        #! window division
        self._setupFrames()
        self._setupWidgetsTopFrame()
        self._setupWidgetsMiddleFrame()
        self._setupWidgetsBottomFrame()

        self.r.bind('<Return>', self.sendfunction)
        self.r.protocol("WM_DELETE_WINDOW", quit)

        self.msgBuffer = []
        self.vlcFrames = []
        self.vlcInstances = []
        self.vlcPlayer = []
        self.vlcMedias = []
        self.vlcButtons = []
        self.mediaFrames = []

        self.tempImageCanvas = []

        self.audioImage = ImageTk.PhotoImage(Image.open(r'gui\audio.png'))

    def run(self):
        if not self.isRunning:
            self.r.mainloop()
        self.isRunning = True

    def _setupFrames(self):
        self.fr_top = tkinter.Frame(master=self.r, bg='black', width=800)
        self.fr_middle = tkinter.Frame(master=self.r, bg='black', width=800)
        self.fr_bottom = tkinter.Frame(master=self.r, bg='black', width=800)

        self.fr_top.place(relheight=0.15, relwidth=1)
        self.fr_middle.place(relheight=0.75, relwidth=1, rely=0.15)
        self.fr_bottom.place(relheight=0.1, relwidth=1, rely=0.9)

    def _setupWidgetsTopFrame(self):
        self.cv_Topframe = tkinter.Canvas(
            master=self.fr_top, bg='black', borderwidth=0, highlightthickness=0)
        self.cv_Topframe.pack(fill='both', expand=True)

        bluerectCoord = 0, 0, 800, 40
        self.cv_Topframe.create_rectangle(bluerectCoord, fill=BLUE)

        limitlineCoord = 0, 600*0.14, 800, 600*0.14
        self.cv_Topframe.create_line(limitlineCoord, fill=BLUE)

        imgpos = 12, 2, 15+73, 5+73
        self.cv_Topframe.create_oval(imgpos, fill=BLUE)

        self.cv_Topframe.create_image(
            13.5+36.5, 3.5+36.5, image=self.friendPFP)

        self.cv_Topframe.create_text(
            96, 53, text=f"{self.friendNick}", fill=LBLUE, font=("Ubuntu 20 bold"), anchor='w')
        self.cv_Topframe.create_text(
            97, 68, text=f"{self.friendStatus}", fill=LBLUE, font=("Ubuntu 9 bold"), anchor='w')
        self.cv_Topframe.create_text(
            96, 78, text="Status:", fill=LBLUE, font=("Ubuntu 9 bold"), anchor='w')
        self.cv_Topframe.create_text(
            145, 78, text=f"{self.friendCustomStatus}", fill=HBLUE, font=("Ubuntu 9"), anchor='w')

        self.pausebuttonimg = ImageTk.PhotoImage(Image.open(r'gui\Resume.png'))

    def _setupWidgetsMiddleFrame(self):
        self.text_MiddleFrame = tkinter.scrolledtext.ScrolledText(master=self.fr_middle, wrap=tkinter.WORD, bg='black', borderwidth=0, highlightthickness=0, font=(
            'ubuntu 12'), foreground=HBLUE, selectbackground=HBLUE, state=DISABLED)
        self.text_MiddleFrame.pack(expand=True, fill=BOTH)
        #self.text_MiddleFrame.place(x=13.5, y=10, relheight=600-10, width=800-13.5)
        self.lastcurtime = ''

    def _setupWidgetsBottomFrame(self):
        self.isPlus = False
        self.tempFiles = []

        self.fr_CU = tkinter.Canvas(master=self.fr_middle, bg=BLUE, borderwidth=0,
                                    highlightcolor=LBLUE, highlightthickness=0, height=50, width=80)
        self.imgbtup = ImageTk.PhotoImage(Image.open(r"gui\up.png"))
        self.imgbtclear = ImageTk.PhotoImage(Image.open(r"gui\clear.png"))
        self.bt_clear = tkinter.Button(master=self.fr_CU, bg='black', relief=FLAT,
                                       image=self.imgbtclear, activebackground=RED, command=self.clear, cursor=CURSOR)
        self.bt_up = tkinter.Button(master=self.fr_CU, bg='black', relief=FLAT,
                                    image=self.imgbtup, activebackground=BLUE, command=self.upload, cursor=CURSOR)
        self.wasCleared = False

        self.fr_CU.place(height=50, width=80, relx=20, y=300)
        self.bt_clear.place(relheight=0.45, relwidth=0.96, y=2, x=2)
        self.bt_up.place(relheight=0.45, relwidth=0.96, y=50/2 + 1, x=2)

        self.fr_CU.place_forget()

        self.cv_BottomFrame = tkinter.Canvas(
            master=self.fr_bottom, bg='black', borderwidth=0, highlightthickness=0)
        self.cv_BottomFrame.place(relheight=1, relwidth=1)

        limitlineCoord = 0, 3, 800, 3
        self.cv_BottomFrame.create_line(limitlineCoord, fill=BLUE)

        circleCoord2 = 11, 11, 11+40, 11+40
        self.cv_BottomFrame.create_oval(
            circleCoord2, fill='black', outline=BLUE)

        circleCoord2 = 748, 11, 748+40, 11+40
        self.cv_BottomFrame.create_oval(
            circleCoord2, fill='black', outline=BLUE)

        recCoord = 25, 0+12, 800-25, 48+2
        self.cv_BottomFrame.create_rectangle(
            recCoord, fill='black', outline=BLUE)

        linecoord1 = 26, 0+13, 26, 48+1
        self.cv_BottomFrame.create_line(linecoord1, fill='black', width=2)

        linecoord2 = 775, 0+13, 775, 48+1
        self.cv_BottomFrame.create_line(linecoord2, fill='black', width=2)

        self.EntryBottomFrame = tkinter.Entry(master=self.fr_bottom, bg='black', fg=LBLUE, font=(
            'Ubuntu 12'), relief=FLAT, insertbackground=LBLUE)
        self.EntryBottomFrame.place(
            x=60, rely=0.25, relwidth=0.85, relheight=0.5)
        self.EntryBottomFrame.focus()

        self.imgbuttonup = ImageTk.PhotoImage(Image.open(r"gui\plus.png"))
        self.bt_upload = tkinter.Button(master=self.fr_bottom, bg='black', relief=FLAT,
                                        image=self.imgbuttonup, activebackground=BLUE, command=self.plusfunction, cursor=CURSOR)
        self.bt_upload.place(x=22, y=18, height=25, width=25)

        self.imgbuttonsend = ImageTk.PhotoImage(Image.open(r"gui\send.png"))
        self.bt_send = tkinter.Button(master=self.fr_bottom, image=self.imgbuttonsend, bg='black',
                                      relief=FLAT, activebackground=BLUE, command=self.sendfunction, cursor=CURSOR)
        self.bt_send.place(x=753, y=18, height=25, width=25)

    def plusfunction(self):
        if self.isPlus:
            self.fr_CU.place_forget()
            self.isPlus = False
        else:
            self.fr_CU.place(height=50, width=80, x=10, y=390)
            self.isPlus = True

    def sendfunction(self, event=None):
        msg = self.EntryBottomFrame.get()
        self.EntryBottomFrame.delete(0, 'end')

        if self.printfunction(msg=msg):
            time = datetime.now()
            curtime = time.strftime("%H:%M")
            msg = msg.strip()
            sender = self.myNick
            self.text_MiddleFrame.see('end')
            return (curtime, msg)

    def clear(self):
        self.text_MiddleFrame['state'] = tkinter.NORMAL
        self.text_MiddleFrame.delete(1.0, tkinter.END)
        self.text_MiddleFrame['state'] = tkinter.DISABLED
        self.fr_CU.place_forget()
        self.wasCleared = True
        self.isPlus = False

        for player in self.vlcPlayer:
            player.stop()

        self.vlcFrames = []
        self.vlcInstances = []
        self.vlcPlayer = []
        self.vlcMedias = []
        self.vlcButtons = []
        self.mediaFrames = []

        self.tempImageCanvas = []

    def upload(self):
        try:
            self.isPlus = False
            self.fr_CU.place_forget()
            tkinter.Tk().withdraw()
            self.files = filedialog.askopenfilenames()
            print(self.files[0][-3:])
            for file in self.files:
                if file[-4:] in IMAGEEXT:
                    self.printfunction(msg=file, msgtype='image')
                else:
                    self.printfunction(msg=file, msgtype='batata')
                self.msgBuffer.append((True,file))
                self.text_MiddleFrame.see('end')
        except:
            print("Deu erro :(")

    def printfunction(self, me=True, time='', msg='', msgtype='text'):
        if msgtype == 'text':
            msg = msg.strip()
            if msg == '':
                return False
            self.msgBuffer.append(0,msg)

        self.text_MiddleFrame['state'] = tkinter.NORMAL
        time = datetime.now()
        curtime = time.strftime("%H:%M")
        if curtime != self.lastcurtime or self.lastsender != me or self.wasCleared:
            self.wasCleared = False

            nick = f"   {self.myNick if me else self.friendNick}\n"
            self.text_MiddleFrame.insert(tkinter.END, '\n')
            self.text_MiddleFrame.image_create(
                tkinter.END, image=(self.myPFP if me else self.friendPFP))

            curline = int(self.text_MiddleFrame.index('end').split('.')[0])-1

            self.text_MiddleFrame.insert(tkinter.END, nick)

            self.text_MiddleFrame.tag_add(
                'nick', f'{curline}.0', f'{curline}.end')
            self.text_MiddleFrame.tag_config(
                'nick', font='Unbutu 15 bold', foreground=LBLUE)

        if msgtype == 'text':
            msg = f'[{(curtime if me else time)}]:    ' + msg + '\n'
            self.text_MiddleFrame.insert(tkinter.END, msg)

        elif msgtype == 'image':
            time = f'[{(curtime if me else time)}]:    '
            self.text_MiddleFrame.insert(tkinter.END, time)

            self.tempImageCanvas.append(tkinter.Canvas(
                master=self.text_MiddleFrame, height=300, width=400, bg=LBLUE, highlightthickness=0, border=0))
            self.text_MiddleFrame.window_create(
                END, window=self.tempImageCanvas[-1])

            self.tempFiles.append(ImageTk.PhotoImage(
                Image.open(msg).resize((398, 298), Image.ANTIALIAS)))

            self.tempImageCanvas[-1].create_image(
                1, 1, image=self.tempFiles[-1], anchor=tkinter.NW)
            self.text_MiddleFrame.insert(tkinter.END, '\n\n')

        else:
            # vlc media
            time = f'[{(curtime if me else time)}]:    '
            self.text_MiddleFrame.insert(tkinter.END, time)

            self.mediaFrames.append(tkinter.Frame(
                master=self.text_MiddleFrame, height=300, width=400, bg=LBLUE, highlightthickness=0, border=0))
            self.text_MiddleFrame.window_create(
                END, window=self.mediaFrames[-1])

            self.vlcFrames.append(tkinter.Frame(
                master=self.mediaFrames[-1], height=260, width=396, bg='black'))
            self.vlcFrames[-1].place(y=2, x=2)

            self.vlcButtons.append(tkinter.Button(master=self.mediaFrames[-1], bg='black', relief=FLAT, image=self.pausebuttonimg, activebackground=BLUE, command=(
                lambda a=len(self.mediaFrames)-1: self.vlcPlayer[a].set_pause(self.vlcPlayer[a].is_playing())), cursor=CURSOR))
            self.vlcButtons[-1].place(y=260, width=396, x=2, height=38)

            self.vlcInstances.append(vlc.Instance())
            self.vlcPlayer.append(self.vlcInstances[-1].media_player_new())
            self.vlcMedias.append(self.vlcInstances[-1].media_new(msg))
            self.vlcPlayer[-1].set_hwnd(self.vlcFrames[-1].winfo_id())
            self.vlcPlayer[-1].set_media(self.vlcMedias[-1])

            try:
                self.vlcPlayer[-1].audio_set_volume(80)
            except:
                print("porra, imagem não tem audio")
            self.vlcPlayer[-1].play()
            if msg[-4:] in AUDIOEXT:
                self.temp
            self.text_MiddleFrame.insert(tkinter.END, '\n\n')

        curline = int(self.text_MiddleFrame.index('end').split('.')[0])-1
        self.lastcurtime = curtime

        self.lastsender = me
        self.text_MiddleFrame['state'] = tkinter.DISABLED
        return True

    def setProfilesCfg(self):
        self.myPFP = ImageTk.PhotoImage(Image.open(MYPFP))
        self.myNick = MYNICK
        self.myStatus = MYSTATUS
        self.myCustomStatus = MYCUSTOMSTATUS

        self.friendPFP = ImageTk.PhotoImage(Image.open(FRIENDPFP))
        self.friendNick = FRIENDNICK
        self.friendStatus = FRIENDSTATUS
        self.friendCustomStatus = FRIENDCUSTOMSTATUS

        self.lastsender = True

    def setStatus(self, online=True):
        self.myStatus = ("Online" if online else "Offline")

    def setNick(self, nick="Bot"):
        self.myNick = nick

    def setCustomStatus(self, customStatus="Vagabundeando"):
        self.myCustomStatus = customStatus

    def clickedframe(self, event):
        print("porra")
        print(event.widget.widget)


if __name__ == "__main__":
    tk = Gui()

    tk.run()
