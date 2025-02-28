from threading import Thread
import socket
import asyncio


async def read(reader):
    while True:
        data = await reader.read(1024)
        print(f"from client {data.decode()}")


async def write(writer):
    while True:
        msg = await asyncio.to_thread(input, "to client: ")
        writer.write(msg.encode())
        await writer.drain()


async def handler(reader, writer):
    t1 = asyncio.create_task(read(reader))
    t2 = asyncio.create_task(write(writer))
    await asyncio.gather(t1, t2)


async def main():
    serv = await asyncio.start_server(handler, "127.0.0.1", 9000)
    async with serv as s:
        await s.serve_forever()


clients = dict()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    ip_choice = int(input("Local-network IP adress or localhost(1/2): "))
    if ip_choice == 1:
        IP = socket.gethostbyname(socket.gethostname())  # doesn't work on linux
        print(f"Your ip in local network is {IP}")
    else:
        IP = "localhost"
        print("You ip is 127.0.0.1")
    PORT = int(input("Enter port: "))
    server.bind((IP, PORT))
    server.listen(5)
    print("You started listening to ports on incoming connections")
except Exception as e:
    print("Invalid IP or port:", e)


def accept_connection():
    global s
    s = 0
    while True:
        try:
            client, addr = server.accept()
            print("Connected by", addr)
            clients[client] = addr
            print(clients)
            s += 1
            t3 = Thread(
                target=recv_from_client, args=(client, addr, len(clients.keys()))
            )
            t3.start()
        except Exception as e:
            print(e)
            server.close()
            return


def recv_from_client(client, addr, le):
    global s
    while True:
        try:
            data = client.recv(4096)
            datt = f"\nMessage from client({addr}): {data.decode()}".encode()
            print(datt.decode())
            for i in clients.keys():
                i.send(datt)
            Thread(target=send_message, args=(client, s)).start()
            s = 0
        except Exception as e:
            print(e)
            server.close()
            client.close()
            return


def send_message(client, arg):
    if arg == 1:
        client.send(b"You are connected!")

    while True:
        try:
            response = input("Enter your message: ")
            for i in clients.keys():
                i.send(response.encode())
            if response == "quit":
                server.close()
                return
        except Exception as e:
            print(e)
            server.close()
            client.close()
            return


def event_loop():
    t2 = Thread(target=accept_connection)

    t2.start()
    t2.join()


if __name__ == "__main__":
    event_loop()
