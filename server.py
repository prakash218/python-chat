import socket
import threading
from flask import Flask
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname('localhost')
# SERVER = ''
print(SERVER)
ADDR = (SERVER,PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "quit"

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)

global connections

connections = []

app = Flask(__name__)
@app.route('/')
def home():
    return f'Server hosted on {SERVER}'

def handle_client(conn,addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    connections.append(conn)
    while connected:
        try:

            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg.lower == DISCONNECT_MESSAGE:
                    connected = False
                print(f"[{addr}] {msg}")
                for i in connections:
                    try:
                        i.send(msg.encode((FORMAT)))
                    except:
                        continue
        except:
            conn.close()    
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    app.run(host=SERVER, port=1234, debug=True)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
    print('returning')

print("[Starting ] server is starting....")
if __name__ == "__main__":
    start()
    
