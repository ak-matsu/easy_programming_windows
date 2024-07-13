import socket
import tkinter as tk
from ping3 import ping, verbose_ping
from threading import Thread
import time
import netifaces
import requests

def get_local_ip():
    """ローカルIPアドレスを取得する"""
    socket_obj = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        socket_obj.connect(('10.255.255.255', 1))
        IP = socket_obj.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        socket_obj.close()
    return IP

def get_default_gateway():
    """デフォルトゲートウェイを取得する"""
    gateways = netifaces.gateways()
    return gateways['default'][netifaces.AF_INET][0]

def get_global_ip():
    """グローバルIPアドレスを取得する"""
    try:
        response = requests.get('https://api.ipify.org')
        return response.text
    except Exception:
        return None

def check_ping(host, text_widget, start_flag, stats_dict):
    """指定したホストに対してpingを送信し、結果をテキストウィジェットに表示する"""
    text_widget.insert(tk.END, f'{host} に ping を送信しています:\n')
    while start_flag[0]:
        result = ping(host)
        if result is None:
            result_str = f'{host} からの応答: 時間 =N/A ms TTL=N/A\n'
            stats_dict[host]['loss'] += 1
        else:
            result_str = f'{host} からの応答: 時間 ={int(result*1000)}ms TTL=58\n'
            stats_dict[host]['min'] = min(stats_dict[host]['min'], result) if stats_dict[host]['min'] is not None else result
            stats_dict[host]['max'] = max(stats_dict[host]['max'], result) if stats_dict[host]['max'] is not None else result
            stats_dict[host]['total'] += result
            stats_dict[host]['count'] += 1
        text_widget.insert(tk.END, result_str)
        text_widget.see(tk.END)
        time.sleep(1)
        
    # Display statistics when ping stops
    if stats_dict[host]['count'] > 0:
        avg = stats_dict[host]['total'] / stats_dict[host]['count']
        loss_percent = (stats_dict[host]['loss'] / (stats_dict[host]['count'] + stats_dict[host]['loss'])) * 100
        stats_str = f'\n{host} の ping 統計:\n    パケット数: 送信 = {stats_dict[host]["count"] + stats_dict[host]["loss"]}、受信 = {stats_dict[host]["count"]}、損失 = {stats_dict[host]["loss"]} ({loss_percent}% の損失)、\nラウンド トリップの概算時間 (ミリ秒):\n    最小 = {int(stats_dict[host]["min"]*1000)}ms、最大 = {int(stats_dict[host]["max"]*1000)}ms、平均 = {int(avg*1000)}ms\n\n'
        text_widget.insert(tk.END, stats_str)
        text_widget.see(tk.END)

root = tk.Tk()
labels = [tk.Label(root, text=label) for label in ['ループバックアドレス', 'ローカルIP', 'ルータ（デフォルトゲートウェイ）', '外部サーバ', 'グローバルIP']]
texts = [tk.Text(root) for _ in range(5)]
start_flag = [False]
stats_dict = {host: {'min': None, 'max': None, 'total': 0, 'count': 0, 'loss': 0} for host in ['127.0.0.1', get_local_ip(), get_default_gateway(), '8.8.8.8', get_global_ip()]}
def toggle_start():
    """pingの開始/停止を切り替える"""
    start_flag[0] = not start_flag[0]
    if start_flag[0]:
        button.config(text='停止', bg='red')
        for host, text_widget in zip(['127.0.0.1', get_local_ip(), get_default_gateway(), '8.8.8.8', get_global_ip()], texts):
            Thread(target=check_ping, args=(host, text_widget, start_flag, stats_dict), daemon=True).start()
    else:
        button.config(text='開始', bg='green')

button = tk.Button(root, text='開始', command=toggle_start, bg='green')
time_label = tk.Label(root, text='', font=('Helvetica', '16'))
time_label.grid(row=5, column=1, columnspan=2)

def update_time():
    """現在時刻を更新する"""
    current_time = time.strftime('%Y/%m/%d %H:%M:%S')
    time_label.config(text=current_time)
    root.after(1000, update_time)

update_time()

# Place the labels, text boxes and button in the desired layout
for i in range(3):
    labels[i].grid(row=0, column=i)
    texts[i].grid(row=1, column=i)
for i in range(3, 5):
    labels[i].grid(row=2, column=i-3)
    texts[i].grid(row=3, column=i-3)
button.grid(row=5, column=0, columnspan=2)    # Start Ping button

root.mainloop()
