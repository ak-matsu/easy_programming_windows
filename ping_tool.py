import socket
import tkinter as tk
from ping3 import ping
from threading import Thread
import time

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def check_ping(host, text):
    while True:
        result = ping(host)
        if result is None:
            result_str = f'{host} is unreachable\n'
        else:
            result_str = f'{host} is reachable in {result} ms\n'
        text.insert(tk.END, result_str)
        text.see(tk.END)
        time.sleep(1)

root = tk.Tk()
texts = [tk.Text(root) for _ in range(5)]
button = tk.Button(root, text='Start Ping', command=lambda: [Thread(target=check_ping, args=(host, text), daemon=True).start() for host, text in zip(['127.0.0.1', get_local_ip(), 'ルータのIP', 'デフォルトゲートウェイのIP', '8.8.8.8'], texts)])

# Place the text boxes and button in the desired layout
texts[0].grid(row=0, column=0)  # Loopback address
texts[1].grid(row=0, column=1)  # Local network
texts[2].grid(row=0, column=2)  # Router
texts[3].grid(row=1, column=0)  # Default gateway
texts[4].grid(row=1, column=1)  # External server
button.grid(row=1, column=2)    # Start Ping button

root.mainloop()
