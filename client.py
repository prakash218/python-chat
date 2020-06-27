import socket
from tkinter import *
import time
import threading

global box

HEADER = 64
PORT = 5050 
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"
SERVER = "192.168.43.195"
# SERVER = "27.62.27.39"
ADDR = (SERVER,PORT)


client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
try:
    client.connect(ADDR)
except :
    print("Server is down")

i = 0
def receive(message = 'None'):
    global i
    while True:
        try:
            message = client.recv(2000).decode(FORMAT)
            i += 1
            message = message.split(':')
            if message[0] != user:
                Label(frame1,text = message[0] + ':',bg = 'lightblue').grid(row = i+1, column = 1,sticky = 'w')
                Label(frame1,text = message[1],bg = 'lightblue').grid(row = i+1,column = 2,sticky = 'w')
            else:
                Label(frame1,text = message[0] + ':').grid(row = i+1, column = 1,sticky = 'w')
                Label(frame1,text = message[1]+' ' * (1000 - len(message[1]))).grid(row = i+1,column = 2,sticky = 'w')
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
            canvas.configure(scrollregion=canvas.bbox('all'), xscrollcommand=scroll_x.set)
            canvas.pack(fill='both', expand=True, side='left')

            root.update()
        except :
            break
    if message != 'None':
        i += 1
        message = message.split(':')
        if message[0] != user:
            Label(frame1,text = message[0] + ':',bg = 'lightblue').grid(row = i+1, column = 1,sticky = 'w')
            Label(frame1,text = message[1],bg = 'lightblue').grid(row = i+1,column = 2,sticky = 'w')
        else:
            Label(frame1,text = message[0] + ':').grid(row = i+1, column = 1,sticky = 'w')
            Label(frame1,text = message[1]+' ' * (1000 - len(message[1]))).grid(row = i+1,column = 2,sticky = 'w')
        canvas.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
        canvas.configure(scrollregion=canvas.bbox('all'), xscrollcommand=scroll_x.set)
        canvas.pack(fill='both', expand=True, side='left')

        root.update()

def write(name):
    global box
    f = open('Username.txt', 'w+')
    f.write(name.get())
    f.close()
    box.destroy()

def first():
    global box
    box = Tk()
    box.geometry('300x100')
    
    Label(box,text = "User name:").grid(row = 1,column = 1,pady = 15,padx = 15)
    name = StringVar()
    entry = Entry(box,textvariable = name).grid(row = 1, column = 2, padx = 10)
    Button(box, text = "Submit",command = lambda : write(name)).grid(row = 2,column = 2,pady = 15)
    box.mainloop()

def send( n = 5):
    message = msg.get()
    msg.set('')
    send = user+ ':' + message
    message = send.encode(FORMAT) 
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER -  len(send_length))
    try:        
        client.send(send_length)
        client.send(message)
    except :
        receive(send)



started = False
# try:
#     f = open()

while True:
    f = open("Username.txt","r+")
    lines = f.readlines()
    if len(lines) != 0:
        started = True
        break
    else:
        first()


f = open("Username.txt","r+")
lines = f.readlines()
user = lines[0]


if started:
    root = Tk()
    root.geometry('400x600')
    # root.resizable(False,False)
    root.bind('<Return>',send)
    frame = Frame(root).place(x = 0,y = 0)

    canvas = Canvas(frame,bg = "lightblue")
    scroll_y = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scroll_x = Scrollbar(frame, orient="horizontal",command= canvas.xview)
    frame1 = Frame(canvas,relief = RAISED,bg = 'lightblue')

    canvas.create_window(0, 0, anchor='nw', window=frame1)
    canvas.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox('all'), yscrollcommand=scroll_y.set)
    canvas.configure(scrollregion=canvas.bbox('all'), xscrollcommand=scroll_x.set)
    canvas.pack(fill='both', expand=True, side='left')
    scroll_y.pack(fill='y', side='right')
    scroll_x.place(x=0,y=582,width = 381)

    # label = Label(root,text = "Chat messenger",font = ('helvitica',15)).place(x = 80,y = 10)
    Label(root,text = "Message:").place(x = 25,y = 500)
    msg = StringVar()
    Entry(root,textvariable = msg).place(x = 100,y = 500)
    Button(root,text = 'Send',command = send).place(x = 240,y = 500)

thread = threading.Thread(target=receive)
thread.start()
root.mainloop()