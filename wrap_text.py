import tkinter as tk

# Tkinterのウィンドウを作成する
root = tk.Tk()
root.geometry("480x270")

# 出力用のテキストボックスを作成する
text_box = tk.Text(root, width=30, height=10, wrap="char")
text_box.pack()

# エントリーを作成する
entry = tk.Entry(root)
entry.pack()

# エントリーに入力された文字列を30文字か句点で分割して改行する
def on_input(event):
    text = event.widget.get()
    wrapped_text = ""
    while len(text) > 30:
        if "。" in text[:30]:
            index = text[:30].index("。")
            wrapped_text += text[:index+1] + "\n"
            text = text[index+1:]
        else:
            wrapped_text += text[:30] + "\n"
            text = text[30:]
    wrapped_text += text
    text_box.insert("end", wrapped_text)

# エントリーでキーが押されたときに、on_input関数を呼び出す
entry.bind("<Key>", on_input)

# 「クリア」ボタンを作成する
clear_button = tk.Button(root, text="クリア", command=lambda: (entry.delete(0, "end"), text_box.delete("1.0", "end")))
clear_button.pack()

root.mainloop()
