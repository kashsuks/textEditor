import tkinter as tk
from tkinter import filedialog, ttk

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.file_paths = {}  # To store file paths for each tab
        self.tab_counter = 1  # Counter to name new tabs

        self.create_widgets()

    def create_widgets(self):
        # Create a menu bar
        menubar = tk.Menu(self.root)

        # Create the "File" menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New File (Ctrl+N)", command=self.new_file)
        file_menu.add_command(label="Open File (Ctrl+O)", command=self.open_file)
        file_menu.add_command(label="Save (Ctrl+S)", command=self.save_file)
        file_menu.add_command(label="Save As (Ctrl+Shift+S)", command=self.save_as)
        menubar.add_cascade(label="File", menu=file_menu)

        # Create the "Edit" menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo (Ctrl+Z)", command=self.undo)
        edit_menu.add_command(label="Redo (Ctrl+Y)", command=self.redo)
        edit_menu.add_separator()  # Separator between undo/redo and cut/copy/paste
        edit_menu.add_command(label="Cut (Ctrl+X)", command=self.cut)
        edit_menu.add_command(label="Copy (Ctrl+C)", command=self.copy)
        edit_menu.add_command(label="Paste (Ctrl+V)", command=self.paste)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Add the menu bar to the root window
        self.root.config(menu=menubar)

        # Create a tab control
        self.tab_control = ttk.Notebook(self.root)
        self.tab_control.pack(expand=1, fill='both')

        # Create the first tab
        self.new_file()

        # Bind keyboard shortcuts
        self.root.bind('<Control-s>', lambda event: self.save_file())
        self.root.bind('<Control-S>', lambda event: self.save_as())
        self.root.bind('<Control-n>', lambda event: self.new_file())
        self.root.bind('<Control-o>', lambda event: self.open_file())
        self.root.bind('<Control-z>', lambda event: self.undo())
        self.root.bind('<Control-y>', lambda event: self.redo())
        self.root.bind('<Control-x>', lambda event: self.cut())
        self.root.bind('<Control-c>', lambda event: self.copy())
        self.root.bind('<Control-v>', lambda event: self.paste())

    def new_file(self, event=None):
        """Creates a new tab for a new file."""
        text_area = tk.Text(self.tab_control)
        tab_name = f"Untitled-{self.tab_counter}"
        self.file_paths[tab_name] = None  # No path yet for new files
        self.tab_control.add(text_area, text=tab_name)
        self.tab_control.select(text_area)
        self.tab_counter += 1

    def open_file(self, event=None):
        """Opens an existing file."""
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                
            text_area = tk.Text(self.tab_control)
            tab_name = file_path.split("/")[-1]  # Get the file name from the path
            self.file_paths[tab_name] = file_path  # Store the file path for the tab
            self.tab_control.add(text_area, text=tab_name)
            text_area.insert(tk.END, content)
            self.tab_control.select(text_area)

    def save_file(self, event=None):
        """Saves the current file in the active tab."""
        current_tab = self.tab_control.select()
        tab_text = self.tab_control.tab(current_tab, "text")
        
        if self.file_paths[tab_text]:
            # If the file has already been saved before, save directly
            with open(self.file_paths[tab_text], 'w') as file:
                file.write(self.get_text_content())
        else:
            # If it's a new file, call save as
            self.save_as()

    def save_as(self, event=None):
        """Save the current file as a new file."""
        current_tab = self.tab_control.select()
        tab_text = self.tab_control.tab(current_tab, "text")
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text files", "*.txt"),
                                                            ("All files", "*.*")])
        if file_path:
            self.file_paths[tab_text] = file_path  # Update file path for the current tab
            with open(file_path, 'w') as file:
                file.write(self.get_text_content())
            self.tab_control.tab(current_tab, text=file_path.split("/")[-1])  # Update tab title

    def get_text_content(self):
        """Returns the content of the current tab's text area."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        return text_widget.get("1.0", tk.END)

    def undo(self, event=None):
        """Undo the last action."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        text_widget.event_generate("<<Undo>>")

    def redo(self, event=None):
        """Redo the last undone action."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        text_widget.event_generate("<<Redo>>")

    def cut(self, event=None):
        """Cut the selected text."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        text_widget.event_generate("<<Cut>>")

    def copy(self, event=None):
        """Copy the selected text."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        text_widget.event_generate("<<Copy>>")

    def paste(self, event=None):
        """Paste from the clipboard."""
        current_tab = self.tab_control.select()
        text_widget = self.tab_control.nametowidget(current_tab)
        text_widget.event_generate("<<Paste>>")


if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
