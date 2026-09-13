import socket
import threading
from datetime import datetime


HOST = "127.0.0.1"
PORT = 5000

clients = {}


# Send a message to all connected clients
def broadcast(message, sender_socket=None):
    for client in list(clients):
        if client != sender_socket:
            try:
                client.send(message.encode())
            except:
                client.close()
                clients.pop(client, None)


# Handle one connected client
def handle_client(client_socket, address):
    username = ""

    try:
        # Receive username
        username = client_socket.recv(1024).decode()

        clients[client_socket] = username

        print(f"{username} connected from {address}")

        # Notify other clients
        time = datetime.now().strftime("%H:%M")

        broadcast(
            f"[{time}] {username} joined the chat.",
            client_socket
        )

        # Keep receiving messages
        while True:
            message = client_socket.recv(1024).decode()

            if not message:
                break

            time = datetime.now().strftime("%H:%M")

            formatted_message = (
                f"[{time}] {username}: {message}"
            )

            print(formatted_message)

            # Send message to other clients
            broadcast(
                formatted_message,
                client_socket
            )

    except (ConnectionResetError, BrokenPipeError):
        pass

    finally:
        # Remove disconnected client
        if client_socket in clients:
            clients.pop(client_socket)

        time = datetime.now().strftime("%H:%M")

        if username:
            broadcast(
                f"[{time}] {username} left the chat."
            )

            print(f"{username} disconnected.")

        client_socket.close()


# Create the server
server = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

# Allow the server to reuse the port
server.setsockopt(
    socket.SOL_SOCKET,
    socket.SO_REUSEADDR,
    1
)

# Bind server to localhost and port
server.bind(
    (HOST, PORT)
)

# Listen for incoming connections
server.listen()

print("================================")
print("   Python Chat Server")
print("================================")
print(f"Server running on {HOST}:{PORT}")
print("Waiting for clients...")


# Accept clients continuously
while True:

    client_socket, address = server.accept()

    # Create a separate thread for each client
    thread = threading.Thread(
        target=handle_client,
        args=(client_socket, address)
    )

    thread.start()