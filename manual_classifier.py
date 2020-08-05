import os
from PIL import ImageTk, Image
from pathlib import Path
import tkinter as tk
import shutil
import pickle

list_of_imgs = []
index = 0
root = tk.Tk()
panel = tk.Label(root)
socket_path = Path("socket")
other_path = Path("other")


def load():
    global index
    if os.path.exists(r'index.dat'):
        with open(r'index.dat', 'rb') as index_file:
            index = pickle.load(index_file)
            print(f'Loaded progress of {index} from saved file')


def save():
    global index
    with open(r'index.dat', 'wb') as index_file:
        pickle.dump(index, index_file)


def classify(socket: bool):
    current = Path(list_of_imgs[index])
    if socket == True:
        shutil.copy2(current, socket_path)
    else:
        shutil.copy2(current, other_path)


def next_img():
    global index
    index += 1
    img = ImageTk.PhotoImage(Image.open(list_of_imgs[index]))
    panel.config(image=img)
    panel.image = img
    panel.pack(side="bottom", fill="both", expand="yes")


def on_press(key):
    global index
    print(f'Key is {key.char}')
    if key.char == 'l':
        classify(False)
        next_img()
        save()
    elif key.char == 's':
        classify(True)
        next_img()
        save()


if __name__ == "__main__":
    load()
    for filename in os.listdir(os.getcwd()):
        if ".jpg" in filename:
            list_of_imgs.append(filename)
    root.title("Bruh")
    root.resizable(False, False)
    root.bind("<KeyPress>", on_press)
    img = ImageTk.PhotoImage(Image.open(list_of_imgs[index]))
    panel.config(image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    tk.mainloop()
