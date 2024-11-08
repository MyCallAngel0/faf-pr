import socket
import threading
import time
import random
import json
from threading import Lock

file_lock = Lock()

file_path = "shared_file.json"

with open(file_path, "w") as file:
    json.dump({"messages": []}, file)

# Server address and port
HOST = '127.0.0.1'
PORT = 65432


def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while True:
        message = conn.recv(1024).decode('utf-8')
        if not message:
            print(f"[DISCONNECT] {addr} disconnected.")
            break

        time.sleep(random.randint(1, 7))

        if message == "read":
            handle_read(conn)
        elif message.startswith("write:"):
            content = message.split(":", 1)[1]
            handle_write(conn, content)
        else:
            conn.sendall(b"Invalid command.\n")

    conn.close()


def handle_read(conn):
    with file_lock:
        with open(file_path, "r") as file:
            data = json.load(file)
            conn.sendall(json.dumps(data).encode('utf-8') + b"\n")
            print("[READ] File content sent to client.")


def handle_write(conn, content):
    with file_lock:
        with open(file_path, "r+") as file:
            data = json.load(file)
            data["messages"].append(content)
            file.seek(0)
            json.dump(data, file)
            file.truncate()

    print(f"[WRITE] Added message: {content}")
    conn.sendall(b"Write operation completed.\n")


def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[LISTENING] Server is listening on {HOST}: {PORT}")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
