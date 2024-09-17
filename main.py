import tkinter as tk
from tkinter import filedialog, Menu

def save_as():
    t = text.get("1.0", "end-1c")
    savelocation = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"),("All files", "*.*")])
    if savelocation:
        try:
            with open(savelocation, "w") as file1:
                file1.write(t)
        except IOError as e:
            print(f"Error saving file: {e}")

def font_helvetica():
    text.config(font="Helvetica")

def font_courier():
    text.config(font="Courier")

root = tk.Tk()
root.title("Text Editor")

text = tk.Text(root)
text.grid()

button = tk.Button(root, text="Save", command=save_as)
button.grid()

font = tk.Menubutton(root, text="Font")
font.grid()
font.menu = Menu(font, tearoff=0)
font["menu"] = font.menu

font.menu.add_checkbutton(label="Courier", command=font_courier)
font.menu.add_checkbutton(label="Helvetica", command=font_helvetica)

root.mainloop()
