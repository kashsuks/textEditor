import tkinter as tk
from tkinter import filedialog, ttk, simpledialog, messagebox
import subprocess
import sys

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Editor")
        self.root.geometry("800x600")

        self.file_paths = {}  # To store file paths for each tab
        self.tab_counter = 1  # Counter to name new tabs

        self.theme = "light"  # Default theme
        self.font_family = "TkDefaultFont"  # Default font
        self.font_size = 12  # Default font size

        self.create_widgets()

    def create_widgets(self):
        # Create a style object
        self.style = ttk.Style()
        
        # Configure default theme styles
        self.style.configure("TFrame", background="#ffffff")  # Default light theme
        self.style.configure("TButton", background="#ffffff", foreground="#000000")
        
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
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut (Ctrl+X)", command=self.cut)
        edit_menu.add_command(label="Copy (Ctrl+C)", command=self.copy)
        edit_menu.add_command(label="Paste (Ctrl+V)", command=self.paste)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Create the "Settings" menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        settings_menu.add_command(label="Font Settings", command=self.open_font_settings)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Create the "Terminal" menu
        terminal_menu = tk.Menu(menubar, tearoff=0)
        terminal_menu.add_command(label="New Terminal", command=self.open_terminal)
        menubar.add_cascade(label="Terminal", menu=terminal_menu)

        # Add the menu bar to the root window
        self.root.config(menu=menubar)

        # Create a custom tab control
        self.tab_frame = ttk.Frame(self.root, style="TFrame")
        self.tab_frame.pack(fill='x')

        self.content_frame = ttk.Frame(self.root, style="TFrame")
        self.content_frame.pack(expand=True, fill='both')

        self.tabs = []  # List to store tab buttons
        self.text_areas = []  # List to store text areas

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

        # Bind window resize event
        self.root.bind('<Configure>', lambda event: self.update_tab_layout())

    def new_file(self, event=None):
        """Creates a new tab for a new file."""
        tab_name = f"Untitled-{self.tab_counter}"
        self.file_paths[tab_name] = None  # No path yet for new files

        # Create a new button for the tab
        tab_button = ttk.Button(self.tab_frame, text=tab_name, command=lambda: self.select_tab(len(self.tabs)), style="TButton")
        self.tabs.append(tab_button)

        # Create a new text area
        text_area = tk.Text(self.content_frame, font=(self.font_family, self.font_size))
        self.text_areas.append(text_area)
        self.apply_theme(text_area)

        self.tab_counter += 1
        self.update_tab_layout()
        self.select_tab(len(self.tabs) - 1)  # Select the newly created tab

    def open_file(self, event=None):
        """Opens an existing file."""
        file_path = filedialog.askopenfilename(defaultextension=".txt",
                                               filetypes=[("Text files", "*.txt"),
                                                          ("All files", "*.*")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            
            tab_name = file_path.split("/")[-1]  # Get the file name from the path
            self.file_paths[tab_name] = file_path  # Store the file path for the tab

            # Create a new button for the tab
            tab_button = ttk.Button(self.tab_frame, text=tab_name, command=lambda: self.select_tab(len(self.tabs)), style="TButton")
            self.tabs.append(tab_button)

            # Create a new text area and insert content
            text_area = tk.Text(self.content_frame, font=(self.font_family, self.font_size))
            text_area.insert(tk.END, content)
            self.text_areas.append(text_area)
            self.apply_theme(text_area)

            self.update_tab_layout()
            self.select_tab(len(self.tabs) - 1)  # Select the newly opened tab

    def save_file(self, event=None):
        """Saves the current file in the active tab."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            tab_text = self.tabs[current_tab_index]['text']
            
            if self.file_paths[tab_text]:
                # If the file has already been saved before, save directly
                with open(self.file_paths[tab_text], 'w') as file:
                    file.write(self.get_text_content(current_tab_index))
            else:
                # If it's a new file, call save as
                self.save_as()

    def save_as(self, event=None):
        """Save the current file as a new file."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     filetypes=[("Text files", "*.txt"),
                                                                ("All files", "*.*")])
            if file_path:
                with open(file_path, 'w') as file:
                    file.write(self.get_text_content(current_tab_index))
                
                # Update tab name and file path
                tab_name = file_path.split("/")[-1]
                self.tabs[current_tab_index]['text'] = tab_name
                self.file_paths[tab_name] = file_path
                self.update_tab_layout()

    def get_text_content(self, tab_index):
        """Returns the content of the specified tab's text area."""
        return self.text_areas[tab_index].get("1.0", tk.END)

    def get_current_tab_index(self):
        """Returns the index of the currently selected tab."""
        for i, text_area in enumerate(self.text_areas):
            if text_area.winfo_viewable():
                return i
        return None

    def select_tab(self, index):
        """Select the tab at the given index."""
        for i, tab in enumerate(self.tabs):
            if i == index:
                tab.config(style='Selected.TButton')
                self.text_areas[i].pack(expand=True, fill='both')
            else:
                tab.config(style='TButton')
                self.text_areas[i].pack_forget()

    def update_tab_layout(self):
        """Update the layout of the tabs and text areas."""
        num_tabs = len(self.tabs)
        if num_tabs > 0:
            width = 100 / num_tabs
            for i, tab in enumerate(self.tabs):
                tab.place(x=width * i, relwidth=width / 100, anchor='nw', height=30)
            for i, text_area in enumerate(self.text_areas):
                text_area.place(x=0, y=30, relwidth=1, relheight=1)

    def undo(self, event=None):
        """Undo the last action."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Undo>>")

    def redo(self, event=None):
        """Redo the last undone action."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Redo>>")

    def cut(self, event=None):
        """Cut text to clipboard."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Cut>>")

    def copy(self, event=None):
        """Copy text to clipboard."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Copy>>")

    def paste(self, event=None):
        """Paste text from clipboard."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Paste>>")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.theme == "light":
            self.theme = "dark"
            bg_color = "#2e2e2e"
            fg_color = "#ffffff"
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TButton", background=bg_color, foreground=fg_color)
            self.root.config(bg=bg_color)
            for text_area in self.text_areas:
                text_area.config(bg=bg_color, fg=fg_color)
                self.apply_theme(text_area)
            self.update_tab_layout()
        else:
            self.theme = "light"
            bg_color = "#ffffff"
            fg_color = "#000000"
            self.style.configure("TFrame", background=bg_color)
            self.style.configure("TButton", background=bg_color, foreground=fg_color)
            self.root.config(bg=bg_color)
            for text_area in self.text_areas:
                text_area.config(bg=bg_color, fg=fg_color)
                self.apply_theme(text_area)
            self.update_tab_layout()

    def apply_theme(self, text_area=None):
        """Apply the current theme to all text areas and the tab frame."""
        bg_color = "#ffffff" if self.theme == "light" else "#2e2e2e"
        fg_color = "#000000" if self.theme == "light" else "#ffffff"
        
        if text_area:
            text_area.config(bg=bg_color, fg=fg_color, insertbackground='white' if self.theme == 'dark' else 'black')

        # Apply the background color using the correct method
        self.style.configure("TFrame", background=bg_color)

    def open_font_settings(self):
        """Open the font settings dialog."""
        font_family = simpledialog.askstring("Font Family", "Enter the font family:", initialvalue=self.font_family)
        if font_family:
            try:
                self.font_family = font_family
                font_size = simpledialog.askinteger("Font Size", "Enter the font size:", initialvalue=self.font_size, minvalue=1)
                if font_size:
                    self.font_size = font_size
                    for text_area in self.text_areas:
                        text_area.config(font=(self.font_family, self.font_size))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to apply font settings: {e}")

    def open_terminal(self):
        """Open a new terminal window."""
        if sys.platform == "win32":
            subprocess.Popen(["start", "cmd"], shell=True)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", "-a", "Terminal"])
        else:
            subprocess.Popen(["gnome-terminal"])  # For Linux-based systems

if __name__ == "__main__":
    root = tk.Tk()
    app = TextEditor(root)
    root.mainloop()
