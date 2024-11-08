import socket
import random
import time

HOST = '127.0.0.1'
PORT = 65432


def send_command(command):
    with socket.create_connection((HOST, PORT)) as sock:
        sock.sendall(command.encode('utf-8'))
        response = sock.recv(1024)
        print(f"Server response: {response.decode('utf-8')}")


# Function to simulate client sending multiple commands
def simulate_client():
    for i in range(11):
        time.sleep(random.randint(1, 7))
        if i % 2 == 0:
            message = "write:" + random.choice([f"Hello\n", f"Bonjour\n", f"Konichiwa\n", f"Gutentag\n", f"Salut\n", f"Zdarova\n"])
            print(f"Sending write command: {message}")
            send_command(message)
        else:
            print(f"Sending read command.")
            send_command("read")


if __name__ == "__main__":
    simulate_client()
