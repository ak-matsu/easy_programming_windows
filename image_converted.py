import os
import subprocess  # 追加
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from tkinterdnd2 import DND_FILES, TkinterDnD

def convert_image(file_path):
    # 保存先フォルダ選択ダイアログを表示
    save_dir = filedialog.askdirectory()
    
    # キャンセルが押された場合
    if not save_dir:
        messagebox.showinfo('Info', 'キャンセルされました')
        return

    # 画像を開く
    img = Image.open(file_path)
    
    # 画像のアスペクト比を維持
    width, height = img.size
    aspect_ratio = width / height
    
    # 1MB以下になるように品質を調整して保存
    for quality in range(100, 0, -1):
        index = 1
        while True:
            save_path = os.path.join(save_dir, f'converted_{index}.jpg')
            if not os.path.exists(save_path):
                break
            index += 1
        img.save(save_path, 'JPEG', quality=quality)
        if os.path.getsize(save_path) <= 1024 * 1024:  # 1MB以下になったら終了
            break
        os.remove(save_path)  # 1MBを超えるファイルは削除

    # 保存先のフォルダを開く
    subprocess.Popen(['explorer', save_dir.replace('/', '\\')])

    messagebox.showinfo('Info', '画像の変換が完了しました')

def drop(event):
    file_path = event.data
    if file_path.endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        root.configure(bg='white')  # ドロップ後は背景色を白に戻す
        convert_image(file_path)
    else:
        messagebox.showinfo('Info', '画像ファイルをドロップしてください')

def drag_enter(event):
    root.configure(bg='lightgreen')  # ドラッグ中は背景色を緑にする

def drag_leave(event):
    root.configure(bg='white')  # ドラッグが終わったら背景色を白に戻す

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('All Files', '*.*')])
    if file_path:
        convert_image(file_path)

# GUIを作成
root = TkinterDnD.Tk()
root.title('Image Converter')
root.geometry('500x500')

drop_area = tk.Label(root, text='ここに画像ファイルをドロップしてください', bd=1, relief='solid')
drop_area.pack(fill='both', expand=True)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)
root.dnd_bind('<<DragEnter>>', drag_enter)
root.dnd_bind('<<DragLeave>>', drag_leave)

btn = tk.Button(root, text='画像を選択', command=select_file)
btn.pack(padx=20, pady=20)

root.mainloop()