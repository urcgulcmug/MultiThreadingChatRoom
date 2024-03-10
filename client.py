import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = input('Enter IP of chat room(or "localhost"): ')
PORT = int(input('Enter the port of chat room: '))
try:

    client.connect((IP, PORT))
except Exception as e:
    client.close()
    print('Invalid IP or port:', e)

def recv_message(client):
    while True:
        try:
            t2 = threading.Thread(target=send_message, args=(client,))
            t2.start()
            data = client.recv(1024)
            print('\nMessage from server:', data.decode())

            if data.decode() == 'q':
                break
        except Exception as e:
            print(e)
            client.close()
            return

def send_message(client):
    while True:
        try:
            message = input('Enter message for server(or "quit"): ')
            if message == 'quit':
                client.close()
                break
            client.send(message.encode())
        except Exception as e:
            print(e)
            client.close()
            return

def event_loop():
    t1 = threading.Thread(target=recv_message, args=(client,))
    t1.start()
    t1.join()

if __name__ == '__main__':
    event_loop()

