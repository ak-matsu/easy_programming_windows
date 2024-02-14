import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy.editor import VideoFileClip

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

def convert_video(file_path, save_dir, max_size_mb=30):
    clip = VideoFileClip(file_path)
    clip_resized = clip.resize(height=360)  # アスペクト比を維持しながら高さを360pxにリサイズ
    index = 1
    while True:
        save_path = os.path.join(save_dir, f'converted_{index}.mp4')
        if not os.path.exists(save_path):
            break
        index += 1
    clip_resized.write_videofile(save_path, codec='libx264', audio_codec='aac', bitrate="2000k")
    if os.path.getsize(save_path) > max_size_mb * 1024 * 1024:  # max_size_mbを超える場合
        os.remove(save_path)  # max_size_mbを超えるファイルは削除
        messagebox.showinfo('Info', '動画のサイズが大きすぎます')
    else:
        messagebox.showinfo('Info', '動画の変換が完了しました')

def select_files(aspect_ratio=None, max_size_kb=50, max_size_mb=30):
    file_paths = filedialog.askopenfilenames(filetypes=[('All Files', '*.*')])
    if not file_paths:
        messagebox.showinfo('Info', 'キャンセルされました')
        return
    save_dir = filedialog.askdirectory()
    if not save_dir:
        messagebox.showinfo('Info', 'キャンセルされました')
        return
    for file_path in file_paths:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            img = Image.open(file_path)
            width, height = img.size
            aspect_ratio = 16/9 if width > height else 4/3
            if abs(width/height - aspect_ratio) > 0.01:  # アスペクト比が近くない場合
                aspect_ratio = width / height  # 元のアスペクト比を維持
            convert_image(file_path, save_dir, aspect_ratio, max_size_kb)
            messagebox.showinfo('Info', '画像の変換が完了しました')
        elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
            convert_video(file_path, save_dir, max_size_mb)
    # 保存先のフォルダを開く
    subprocess.Popen(['explorer', save_dir.replace('/', '\\')])

# GUIを作成
root = tk.Tk()
root.title('Image and Video Converter')
root.geometry('500x500')

frame = tk.Frame(root)
frame.pack(expand=True)

description = tk.Label(root, text="画像は500kb以内に、動画は30mb以内に変換します。\n16:9なら800*450\n4:3なら800*600\n対象外はリサイズ")
description.pack(pady=10)

btn_convert = tk.Button(frame, text='ファイル変換', command=lambda: select_files(max_size_kb=500, max_size_mb=30))
btn_convert.pack(side='left', padx=20, pady=20)

root.mainloop()
