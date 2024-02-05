import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image

def resize_image(img, aspect_ratio):
    width, height = img.size
    if aspect_ratio == 16/9:
        return img.resize((800, 450))
    elif aspect_ratio == 4/3:
        return img.resize((800, 600))
    else:  # アスペクト比が異なる場合
        return img

def convert_image(file_path, save_dir, aspect_ratio=None, max_size_kb=50):
    # 画像を開く
    img = Image.open(file_path)
    
    # アスペクト比に基づいて画像をリサイズ
    if aspect_ratio:
        img = resize_image(img, aspect_ratio)
    
    # RGBA画像をRGBに変換
    if img.mode == 'RGBA':
        img = img.convert('RGB')
    
    # max_size_kb以下になるように品質を調整して保存
    for quality in range(100, 0, -1):
        index = 1
        while True:
            save_path = os.path.join(save_dir, f'converted_{index}.jpg')
            if not os.path.exists(save_path):
                break
            index += 1
        img.save(save_path, 'JPEG', quality=quality)
        if os.path.getsize(save_path) <= max_size_kb * 1024:  # max_size_kb以下になったら終了
            break
        os.remove(save_path)  # max_size_kbを超えるファイルは削除

    # 保存先のフォルダを開く
    subprocess.Popen(['explorer', save_dir.replace('/', '\\')])

    messagebox.showinfo('Info', '画像の変換が完了しました')

def select_file(aspect_ratio=None, max_size_kb=50):
    file_path = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
    if file_path:
        save_dir = filedialog.askdirectory()
        if not save_dir:
            messagebox.showinfo('Info', 'キャンセルされました')
            return
        img = Image.open(file_path)
        width, height = img.size
        aspect_ratio = 16/9 if width > height else 4/3
        if abs(width/height - aspect_ratio) > 0.01:  # アスペクト比が近くない場合
            aspect_ratio = width / height  # 元のアスペクト比を維持
        convert_image(file_path, save_dir, aspect_ratio, max_size_kb)

# GUIを作成
root = tk.Tk()
root.title('Image Converter')
root.geometry('500x500')

frame = tk.Frame(root)
frame.pack(expand=True)

description = tk.Label(root, text="16:9なら800*450、4:3なら800*600\nそれ以外はリサイズと\nそれぞれ500kb以内に変換")
description.pack(pady=10)

btn_convert = tk.Button(frame, text='画像変換', command=lambda: select_file(max_size_kb=500))
btn_convert.pack(side='left', padx=20, pady=20)

root.mainloop()
