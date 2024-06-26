import os
import subprocess
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from moviepy.editor import VideoFileClip

class Converter:
    def __init__(self, max_size_kb=50, max_size_mb=30):
        self.max_size_kb = max_size_kb
        self.max_size_mb = max_size_mb

    def resize_image(self, img, aspect_ratio):
        width, height = img.size
        if aspect_ratio == 16/9:
            return img.resize((800, 450))
        elif aspect_ratio == 4/3:
            return img.resize((800, 600))
        else:
            return img

    def convert_image(self, file_path, save_dir, aspect_ratio=None):
        img = Image.open(file_path)
        if aspect_ratio:
            img = self.resize_image(img, aspect_ratio)
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        for quality in range(100, 0, -1):
            index = 1
            while True:
                save_path = os.path.join(save_dir, f'converted_{index}.jpg')
                if not os.path.exists(save_path):
                    break
                index += 1
            img.save(save_path, 'JPEG', quality=quality)
            if os.path.getsize(save_path) <= self.max_size_kb * 1024:
                break
            os.remove(save_path)

    def convert_video(self, file_path, save_dir):
        clip = VideoFileClip(file_path)
        clip_resized = clip.resize(height=360)
        index = 1
        while True:
            save_path = os.path.join(save_dir, f'converted_{index}.mp4')
            if not os.path.exists(save_path):
                break
            index += 1
        clip_resized.write_videofile(save_path, codec='libx264', audio_codec='aac', bitrate="2000k")
        if os.path.getsize(save_path) > self.max_size_mb * 1024 * 1024:
            os.remove(save_path)
            return False
        else:
            return True

    def select_files(self):
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
                if abs(width/height - aspect_ratio) > 0.01:
                    aspect_ratio = width / height
                self.convert_image(file_path, save_dir, aspect_ratio)
            elif file_path.lower().endswith(('.mp4', '.avi', '.mov')):
                if not self.convert_video(file_path, save_dir):
                    messagebox.showinfo('Info', '動画のサイズが大きすぎます')
                    return
        messagebox.showinfo('Info', '変換が完了しました')
        subprocess.Popen(['explorer', save_dir.replace('/', '\\')])

def create_gui():
    root = tk.Tk()
    root.title('Image and Video Converter')
    root.geometry('500x500')

    frame = tk.Frame(root)
    frame.pack(expand=True)

    description = tk.Label(root, text="画像は500kb以内に、動画は30mb以内に変換します。\n16:9なら800*450\n4:3なら800*600\n対象外はリサイズ")
    description.pack(pady=10)

    converter = Converter(max_size_kb=500, max_size_mb=30)
    btn_convert = tk.Button(frame, text='ファイル変換', command=converter.select_files)
    btn_convert.pack(side='left', padx=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
