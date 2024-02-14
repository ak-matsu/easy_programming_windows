import sys
import os
from PIL import Image
from moviepy.editor import VideoFileClip, concatenate_videoclips
from tqdm import tqdm

class TqdmLogger:
    def __init__(self):
        self.pbar = None

    def __call__(self, message):
        self.write(message)

    def iter_bar(self, t=None, **kwargs):  # t引数を追加して無視
        if self.pbar is None:
            self.pbar = tqdm(**kwargs)
        return self.pbar

    def write(self, s):
        if 'MoviePy - Writing audio' in s:
            self.pbar = tqdm(total=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', file=sys.stdout)  # tqdmの出力をstdoutにリダイレクト
        elif 'MoviePy - Done' in s:
            self.pbar.update(100 - self.pbar.n)
            self.pbar.close()
        elif 'MoviePy - Writing video' in s:
            self.pbar = tqdm(total=100, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}', file=sys.stdout)  # tqdmの出力をstdoutにリダイレクト
        elif '%' in s:
            percent = float(s.split('%')[0].split(' ')[-1])
            self.pbar.update(percent - self.pbar.n)
            print(percent)  # stdoutに進行状況を出力

    def flush(self):
        pass

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
    index = 1
    while True:
        save_path = os.path.join(save_dir, f'converted_{index}.mp4')
        if not os.path.exists(save_path):
            break
        index += 1
    clip = VideoFileClip(file_path)
    print(f"Video duration: {clip.duration} seconds")  # ビデオの長さを表示
    clip_resized = clip.resize(height=360)  # ビデオの高さを360ピクセルにリサイズ

    # ビデオ全体を一度に書き出し、進行状況を更新
    clip_resized.write_videofile(save_path, codec='libx264', bitrate=f'{max_size_mb}M', logger=TqdmLogger())  # progress_bar引数を削除


if __name__ == '__main__':
    file_path = sys.argv[1]
    save_dir = sys.argv[2]
    if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        img = Image.open(file_path)
        width, height = img.size
        aspect_ratio = 16/9 if width > height else 4/3
        if abs(width/height - aspect_ratio) > 0.01:  # アスペクト比が近くない場合
            aspect_ratio = width / height  # 元のアスペクト比を維持
        convert_image(file_path, save_dir, aspect_ratio, max_size_kb=500)
    elif file_path.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        convert_video(file_path, save_dir, max_size_mb=30)