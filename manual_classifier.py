# This is for manually selecting the type of the image (If it's a socket or not)
# This is meant to run under a directory with 1.jpg to n.jpg
# This is for TensorFlow classification

import os
from PIL import ImageTk, Image
from pathlib import Path
import tkinter as tk
import shutil
import pickle

# list_of_imgs = []
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
    current = Path(f'{index}.jpg')
    if socket == True:
        shutil.copy2(current, socket_path)
    else:
        shutil.copy2(current, other_path)


def next_img():
    global index
    index += 1
    if os.path.exists(f'{index}.jpg'):
        img = ImageTk.PhotoImage(Image.open(f'{index}.jpg'))
        panel.config(image=img)
        panel.image = img
        panel.pack(side="bottom", fill="both", expand="yes")
    else:
        print("Not found or reached the end!")
        exit(0)


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

    # Old method and debug commented out here
    # for filename in os.listdir(os.getcwd()):
    #     if ".jpg" in filename:
    #         list_of_imgs.append(filename)
    #
    # i=0
    # for f in list_of_imgs:
    #    i+=1
    #    os.rename(f,f'{i}.jpg')

    root.title("Bruh")
    root.resizable(False, False)
    root.bind("<KeyPress>", on_press)
    img = ImageTk.PhotoImage(Image.open(f'{index}.jpg'))
    panel.config(image=img)
    panel.pack(side="bottom", fill="both", expand="yes")
    tk.mainloop()
