import socket
import tkinter as tk
from ping3 import ping, verbose_ping
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

def check_ping(host, text, start):
    while start[0]:
        result = ping(host)
        if result is None:
            result_str = f'{host} に ping を送信しています 32 バイトのデータ:\n{host} からの応答: バイト数 =32 時間 =N/A ms TTL=N/A\n'
        else:
            result_str = f'{host} に ping を送信しています 32 バイトのデータ:\n{host} からの応答: バイト数 =32 時間 ={int(result*1000)} ms TTL=58\n'
        text.insert(tk.END, result_str)
        text.see(tk.END)
        time.sleep(1)


root = tk.Tk()
labels = [tk.Label(root, text=label) for label in ['ループバックアドレス', 'ローカルIP', 'ルータ', 'デフォルトゲートウェイ', '外部サーバ1', '外部サーバ2']]
texts = [tk.Text(root) for _ in range(6)]
start = [False]
def toggle_start():
    start[0] = not start[0]
    if start[0]:
        button.config(text='停止', bg='red')
        for host, text in zip(['127.0.0.1', get_local_ip(), 'ルータのIP', 'デフォルトゲートウェイのIP', '8.8.8.8', '8.8.4.4'], texts):
            Thread(target=check_ping, args=(host, text, start), daemon=True).start()
    else:
        button.config(text='開始', bg='green')

button = tk.Button(root, text='開始', command=toggle_start, bg='green')

# Place the labels, text boxes and button in the desired layout
for i in range(3):
    labels[i].grid(row=0, column=i)
    texts[i].grid(row=1, column=i)
for i in range(3, 6):
    labels[i].grid(row=2, column=i-3)
    texts[i].grid(row=3, column=i-3)
button.grid(row=4, column=1)    # Start Ping button

root.mainloop()
