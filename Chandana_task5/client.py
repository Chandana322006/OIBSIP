import socket
import threading
import tkinter as tk
from tkinter import messagebox


HOST = "127.0.0.1"
PORT = 5000


# Connect to the server
client_socket = socket.socket(
    socket.AF_INET,
    socket.SOCK_STREAM
)

try:
    client_socket.connect(
        (HOST, PORT)
    )

except ConnectionRefusedError:
    messagebox.showerror(
        "Connection Error",
        "Could not connect to the server.\n"
        "Please start server.py first."
    )
    exit()


# Send username to server
def set_username():
    username = username_entry.get().strip()

    if username == "":
        messagebox.showwarning(
            "Username",
            "Please enter your name."
        )
        return

    client_socket.send(
        username.encode()
    )

    username_frame.pack_forget()
    chat_frame.pack(
        fill="both",
        expand=True
    )

    message_entry.focus()


# Receive messages from server
def receive_messages():

    while True:

        try:
            message = client_socket.recv(
                1024
            ).decode()

            if not message:
                break

            # Display message in chat window
            chat_text.config(
                state="normal"
            )

            chat_text.insert(
                tk.END,
                message + "\n"
            )

            chat_text.config(
                state="disabled"
            )

            chat_text.see(
                tk.END
            )

        except:
            break


# Send message to server
def send_message(event=None):

    message = message_entry.get().strip()

    if message == "":
        return

    try:
        client_socket.send(
            message.encode()
        )

        message_entry.delete(
            0,
            tk.END
        )

    except:
        messagebox.showerror(
            "Error",
            "Message could not be sent."
        )


# Close client
def close_client():

    try:
        client_socket.close()
    except:
        pass

    window.destroy()


# Create GUI window
window = tk.Tk()

window.title(
    "Python Chat Application"
)

window.geometry(
    "600x500"
)

window.protocol(
    "WM_DELETE_WINDOW",
    close_client
)


# -----------------------------------------
# USERNAME FRAME
# -----------------------------------------

username_frame = tk.Frame(
    window
)

username_frame.pack(
    expand=True
)

title_label = tk.Label(
    username_frame,
    text="Python Chat Application",
    font=("Arial", 22, "bold")
)

title_label.pack(
    pady=20
)

username_label = tk.Label(
    username_frame,
    text="Enter your name:",
    font=("Arial", 12)
)

username_label.pack(
    pady=5
)

username_entry = tk.Entry(
    username_frame,
    width=30,
    font=("Arial", 12)
)

username_entry.pack(
    pady=5
)

join_button = tk.Button(
    username_frame,
    text="Join Chat",
    width=15,
    command=set_username
)

join_button.pack(
    pady=15
)


# -----------------------------------------
# CHAT FRAME
# -----------------------------------------

chat_frame = tk.Frame(
    window
)


# Chat display
chat_text = tk.Text(
    chat_frame,
    state="disabled",
    font=("Arial", 11),
    wrap="word"
)

chat_text.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)


# Message input area
input_frame = tk.Frame(
    chat_frame
)

input_frame.pack(
    fill="x",
    padx=10,
    pady=10
)


message_entry = tk.Entry(
    input_frame,
    font=("Arial", 12)
)

message_entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(0, 5)
)


send_button = tk.Button(
    input_frame,
    text="Send",
    width=10,
    command=send_message
)

send_button.pack(
    side="right"
)


# Press Enter to send
message_entry.bind(
    "<Return>",
    send_message
)


# -----------------------------------------
# START RECEIVING THREAD
# -----------------------------------------

receive_thread = threading.Thread(
    target=receive_messages,
    daemon=True
)

receive_thread.start()


# Start GUI
window.mainloop()