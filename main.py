import tkinter as tk
from tkinter import filedialog, Menu

def save_as():
    t = text.get("1.0", "end-1c")
    savelocation = filedialog.asksaveasfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
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

def toggle_fullscreen(event=None):
    global fullscreen
    fullscreen = not fullscreen
    root.attributes("-fullscreen", fullscreen)
    if fullscreen:
        text.config(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    else:
        root.geometry("800x600")  # Set to default window size when exiting fullscreen
        text.config(width=800, height=600)

def exit_fullscreen(event=None):
    global fullscreen
    fullscreen = False
    root.attributes("-fullscreen", False)
    root.geometry("800x600")  # Reset to normal size
    text.config(width=800, height=600)

def handle_configure(event=None):
    global fullscreen
    if root.winfo_width() == root.winfo_screenwidth() and root.winfo_height() == root.winfo_screenheight():
        if not fullscreen:  # Trigger fullscreen mode
            toggle_fullscreen()
    elif not fullscreen and root.state() == 'normal':
        text.config(width=root.winfo_width(), height=root.winfo_height())

root = tk.Tk()
root.title("Text Editor")
root.geometry("800x600")  # Initial window size

fullscreen = False

text = tk.Text(root)
text.grid(sticky="nsew")

# Adjust text widget dynamically to window size
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

button = tk.Button(root, text="Save", command=save_as)
button.grid()

font = tk.Menubutton(root, text="Font")
font.grid()
font.menu = Menu(font, tearoff=0)
font["menu"] = font.menu

font.menu.add_checkbutton(label="Courier", command=font_courier)
font.menu.add_checkbutton(label="Helvetica", command=font_helvetica)

# Bind the F11 key to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

# Bind to <Configure> to track window state changes
root.bind("<Configure>", handle_configure)

root.mainloop()
