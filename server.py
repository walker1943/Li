from tkinter import *
import socket
import threading
import time


class servtk():
    def __init__(self, tk):
        self.tk = tk
        self.tk.geometry('640x480+100+100')
        self.tk.resizable(height=False, width=False)
        self.message = ''
        # setting status frame
        self.frmstus = Frame(self.tk, height=96,
                             width=636, bd=2, relief=RIDGE)
        self.frmstus.grid(row=0, column=0, columnspan=3, padx=2, pady=2)
        self.frmstus.grid_propagate(0)
        self.txtstus = Text(self.frmstus, height=6, width=70)
        self.txtstus.grid(sticky=W)
        self.txtstus.grid_propagate(0)

        # setting msg frm
        self.frmmsgl = Frame(self.tk, height=276, width=246,
                             bg='lightgreen', bd=2, relief=RIDGE)
        self.frmmsgl.grid(row=1, column=0, padx=2, pady=2)
        self.frmmsgl.grid_propagate(0)
        Label(self.frmmsgl, text="Recieved", fg='orange',
              bd=2, relief=SOLID).grid()
        self.frmmsgr = Frame(self.tk, height=276, width=246,
                             bg='lightblue', bd=2, relief=RIDGE)
        self.frmmsgr.grid(row=1, column=1, padx=2, pady=2)
        self.frmmsgr.grid_propagate(0)
        Label(self.frmmsgr, text="Send", fg='orange',
              bd=2, relief=SOLID).grid()

        # setting entry frm
        self.frmety = Frame(self.tk, width=496, height=96, bd=2, relief=RIDGE)
        self.frmety.grid(row=2, column=0, columnspan=2, padx=2, pady=2)
        self.frmety.grid_propagate(0)
        self.txtety = Text(self.frmety, width=60, height=6, bg='white')
        self.txtety.grid(row=0, column=0)
#        self.txtety.bind('<Key>', self.sendmsg)
        self.txtety.grid_propagate(0)
        self.btnsnd = Button(self.frmety, text='send',
                             command=self.sendmsg).grid(row=0, column=1)

        # setting button frm
        self.frmshow = Frame(self.tk, width=134, height=376,
                             bd=2, relief=SOLID)
        self.frmshow.grid(row=1, column=2, rowspan=2, padx=2, pady=2)
        self.frmshow.grid_propagate(0)

    def sendmsg(self):
        self.message = self.txtety.get('1.0', END)
        if self.message != '':
            Label(self.frmmsgr, text=time.ctime()[
                  11:19], fg='blue').grid(sticky=NW)
            Label(self.frmmsgr, text=self.message[:-1],
                  fg='blue', bg='lightblue').grid(sticky=NW)
            self.txtety.delete('0.0', END)
            self.txtety.mark_set('', '0.0')
        else:
            pass


class servsoc():
    def __init__(self, tk):
        self.tk = tk
        self.host = 'localhost'
        self.port = 43532

        self.svrsc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.svrsc.bind((self.host, self.port))
        self.svrsc.listen(10)

        self.tk.txtstus.insert(INSERT, "Start listening...\n")

    def dlg(self, conn):
        conn.settimeout(0.1)
        while True:
            if self.tk.message != '':
                conn.sendall(bytes(self.tk.message, encoding='utf-8'))
                self.tk.message = ''
            try:
                msg = str(conn.recv(1024), encoding='utf-8')
                Label(self.tk.frmmsgl, text=time.ctime()[11:19],
                      bg='lightpink', fg="blue").grid(sticky=NW)
                Label(self.tk.frmmsgl, text=msg, fg='blue',
                      bg='lightgreen').grid(sticky=NW)

            except socket.timeout:
                continue

    def connecting(self):
        while True:
            conn, addr = self.svrsc.accept()
            self.tk.txtstus.insert(INSERT, "connect with {}".format(addr))
            t = threading.Thread(target=self.dlg, args=(conn,))
            t.setDaemon(True)
            t.start()
        conn.close()


def main():
    tk = Tk()
    servgui = servtk(tk)
    server = servsoc(servgui)
    t = threading.Thread(target=server.connecting, args=())
    t.setDaemon(True)
    t.start()
    mainloop()


if __name__ == '__main__':
    main()
