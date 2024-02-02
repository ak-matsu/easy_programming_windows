import socket
import tkinter as tk
from ping3 import ping, verbose_ping
from threading import Thread
import time
import netifaces

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

def get_default_gateway():
    gws = netifaces.gateways()
    return gws['default'][netifaces.AF_INET][0]

def check_ping(host, text, start, stats):
    text.insert(tk.END, f'{host} に ping を送信しています 32 バイトのデータ:\n')
    while start[0]:
        result = ping(host)
        if result is None:
            result_str = f'{host} からの応答: バイト数 =32 時間 =N/A ms TTL=N/A\n'
            stats[host]['loss'] += 1
        else:
            result_str = f'{host} からの応答: バイト数 =32 時間 ={int(result*1000)}ms TTL=58\n'
            stats[host]['min'] = min(stats[host]['min'], result) if stats[host]['min'] is not None else result
            stats[host]['max'] = max(stats[host]['max'], result) if stats[host]['max'] is not None else result
            stats[host]['total'] += result
            stats[host]['count'] += 1
        text.insert(tk.END, result_str)
        text.see(tk.END)
        time.sleep(1)
    # Display statistics when ping stops
    if stats[host]['count'] > 0:
        avg = stats[host]['total'] / stats[host]['count']
        loss_percent = (stats[host]['loss'] / (stats[host]['count'] + stats[host]['loss'])) * 100
        stats_str = f'\n{host} の ping 統計:\n    パケット数: 送信 = {stats[host]["count"] + stats[host]["loss"]}、受信 = {stats[host]["count"]}、損失 = {stats[host]["loss"]} ({loss_percent}% の損失)、\nラウンド トリップの概算時間 (ミリ秒):\n    最小 = {int(stats[host]["min"]*1000)}ms、最大 = {int(stats[host]["max"]*1000)}ms、平均 = {int(avg*1000)}ms\n\n'
        text.insert(tk.END, stats_str)
        text.see(tk.END)

root = tk.Tk()
labels = [tk.Label(root, text=label) for label in ['ループバックアドレス', 'ローカルIP', 'ルータ（デフォルトゲートウェイ）', '外部サーバ']]
texts = [tk.Text(root) for _ in range(4)]
start = [False]
stats = {host: {'min': None, 'max': None, 'total': 0, 'count': 0, 'loss': 0} for host in ['127.0.0.1', get_local_ip(), get_default_gateway(), '8.8.8.8']}
def toggle_start():
    start[0] = not start[0]
    if start[0]:
        button.config(text='停止', bg='red')
        for host, text in zip(['127.0.0.1', get_local_ip(), get_default_gateway(), '8.8.8.8'], texts):
            Thread(target=check_ping, args=(host, text, start, stats), daemon=True).start()
    else:
        button.config(text='開始', bg='green')

button = tk.Button(root, text='開始', command=toggle_start, bg='green')
time_label = tk.Label(root, text='', font=('Helvetica', '16'))
time_label.grid(row=4, column=1, columnspan=2)

def update_time():
    current_time = time.strftime('%Y/%m/%d %H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time)

update_time()

# Place the labels, text boxes and button in the desired layout
for i in range(2):
    labels[i].grid(row=0, column=i)
    texts[i].grid(row=1, column=i)
for i in range(2, 4):
    labels[i].grid(row=2, column=i-2)
    texts[i].grid(row=3, column=i-2)
button.grid(row=4, column=0, columnspan=2)    # Start Ping button

root.mainloop()
