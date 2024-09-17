import tkinter as tk
from tkinter import filedialog, Menu

def save_file():
    # Save to an existing location
    global file_path
    if file_path:
        with open(file_path, 'w') as file:
            file.write(text.get("1.0", "end-1c"))
    else:
        save_as()

def save_as():
    global file_path
    t = text.get("1.0", "end-1c")
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",filetypes=[("Text files", "*.txt"),("All files", "*.*")])
    if file_path:
        try:
            with open(file_path, "w") as file1:
                file1.write(t)
        except IOError as e:
            print(f"Error saving file: {e}")

def open_file():
    global file_path
    file_path = filedialog.askopenfilename(defaultextension=".txt",
                                           filetypes=[("Text files", "*.txt"),
                                                      ("All files", "*.*")])
    if file_path:
        with open(file_path, 'r') as file:
            content = file.read()
            text.delete("1.0", tk.END)  # Clear the text area
            text.insert(tk.END, content)  # Insert file content into text area

def new_file():
    global file_path
    file_path = None
    text.delete("1.0", tk.END)  # Clear the text area for a new file

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

# Initialize the fullscreen variable globally
fullscreen = False
file_path = None

text = tk.Text(root)
text.grid(sticky="nsew")

# Adjust text widget dynamically to window size
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Create a menubar
menubar = Menu(root)

# Create the "File" menu
file_menu = Menu(menubar, tearoff=0)
file_menu.add_command(label="New File", command=new_file)
file_menu.add_command(label="Open File", command=open_file)
file_menu.add_command(label="Save File", command=save_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()  # Adds a horizontal line separator
file_menu.add_command(label="Exit", command=root.quit)

# Add the "File" menu to the menubar
menubar.add_cascade(label="File", menu=file_menu)

# Create the "Font" menu
font_menu = Menu(menubar, tearoff=0)
font_menu.add_command(label="Helvetica", command=font_helvetica)
font_menu.add_command(label="Courier", command=font_courier)

# Add the "Font" menu to the menubar
menubar.add_cascade(label="Font", menu=font_menu)

# Set the menubar to the root window
root.config(menu=menubar)

# Bind the F11 key to toggle fullscreen
root.bind("<F11>", toggle_fullscreen)
root.bind("<Escape>", exit_fullscreen)

# Bind to <Configure> to track window state changes
root.bind("<Configure>", handle_configure)

root.mainloop()
