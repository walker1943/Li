# coding = utf-8
import socket
import time
from tkinter import *
import threading


class clttk():
    def __init__(self, tk):
        self.tk = tk
        self.message = ''
        self.tk.geometry('640x480+100+100')
        self.tk.resizable(height=False, width=False)

        self.frmrecv = Frame(self.tk, height=372,
                             width=300, bd=2, relief=SOLID)
        Label(self.frmrecv, text="recieved", fg='orange').grid(sticky=N)
        self.frmrecv.grid(row=0, column=0, padx=2, pady=2)
        self.frmrecv.grid_propagate(0)

        self.frmsend = Frame(self.tk, height=372,
                             width=300, bd=2, relief=SOLID)
        Label(self.frmsend, text="send", fg='orange').grid(sticky=N)
        self.frmsend.grid(row=0, column=1, padx=2, pady=2)
        self.frmsend.grid_propagate(0)

        self.frmety = Frame(self.tk, width=636, height=100)
        self.frmety.grid(row=1, column=0, columnspan=2, padx=2, pady=2)
        self.frmety.grid_propagate(0)

        self.txtety = Text(self.frmety, width=80, height=5, bd=2, relief=SOLID)
        self.txtety.grid(row=1, column=0, padx=2, pady=2)
        self.txtety.grid_propagate(0)

        self.btnsend = Button(self.frmety, text='send', bd=2,
                              relief=SOLID, command=self.sendmsg)
        self.btnsend.grid(row=1, column=1)
        self.btnsend.grid_propagate(0)

    def sendmsg(self):
        self.message = self.txtety.get('1.0', END)
        if self.message != '':
            Label(self.frmsend, text=time.ctime()[
                  11:19], fg='blue').grid(sticky=NW)
            Label(self.frmsend, text=self.message[:-1],
                  fg='blue', bg='lightblue').grid(sticky=NW)
            self.txtety.delete('0.0', END)
            self.txtety.mark_set('', '0.0')
        else:
            pass


class cltsoc:
    def __init__(self, tk):
        host = '14.117.10.145'
        port = 43532
        self.tk = tk
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((host, port))
        self.client.settimeout(0.1)

    def connecting(self):
        while True:
            if self.tk.message != '':
                self.client.sendall(
                    bytes(self.tk.message, encoding='utf-8'))
                self.tk.message = ''
                self.tk.txtety.delete('1.0', END)
                self.tk.txtety.mark_set('', '0.0')
            try:

                data = str(self.client.recv(1024), encoding='utf-8')
                Label(self.tk.frmrecv, text=time.ctime()[
                      11:19], fg='blue').grid(sticky=NW)
                Label(self.tk.frmrecv, text=data, fg='blue').grid(sticky=NW)

            except socket.timeout:
                continue
        client.close()


def main():
    tk = Tk()
    clienttk = clttk(tk)
    clientsoc = cltsoc(clienttk)
    t = threading.Thread(target=clientsoc.connecting, args=())
    t.setDaemon(True)
    t.start()
    mainloop()

if __name__ == '__main__':
    main()
