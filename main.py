import tkinter as tk
from tkinter import filedialog, ttk, font

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

        # Configure styles
        self.configure_styles()

        self.create_widgets()

    def configure_styles(self):
        """Configure styles for the themes."""
        style = ttk.Style()
        # Light theme styles
        style.configure('Light.TFrame', background='#f0f0f0')
        style.configure('Light.TButton', background='#f0f0f0', borderwidth=0, relief='flat')
        style.configure('Light.TLabel', background='#f0f0f0', foreground='#000000')

        # Dark theme styles
        style.configure('Dark.TFrame', background='#303030')
        style.configure('Dark.TButton', background='#303030', borderwidth=0, relief='flat')
        style.configure('Dark.TLabel', background='#303030', foreground='#ffffff')

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
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut (Ctrl+X)", command=self.cut)
        edit_menu.add_command(label="Copy (Ctrl+C)", command=self.copy)
        edit_menu.add_command(label="Paste (Ctrl+V)", command=self.paste)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Create the "Settings" menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        settings_menu.add_command(label="Toggle Theme", command=self.toggle_theme)
        settings_menu.add_command(label="Change Font", command=self.change_font)
        menubar.add_cascade(label="Settings", menu=settings_menu)

        # Add the menu bar to the root window
        self.root.config(menu=menubar)

        # Create a custom tab control
        self.tab_frame = ttk.Frame(self.root, style='Light.TFrame')
        self.tab_frame.pack(fill='x')

        self.content_frame = ttk.Frame(self.root, style='Light.TFrame')
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
        tab_button = ttk.Button(self.tab_frame, text=tab_name, style='Light.TButton', command=lambda: self.select_tab(len(self.tabs)))
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
            tab_button = ttk.Button(self.tab_frame, text=tab_name, style='Light.TButton', command=lambda: self.select_tab(len(self.tabs)))
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
                tab.config(style='Light.TButton')  # Update the style for selected tab
                self.text_areas[i].pack(expand=True, fill='both')
            else:
                tab.config(style='Light.TButton')  # Update the style for unselected tabs
                self.text_areas[i].pack_forget()

    def update_tab_layout(self):
        """Update the layout of tabs to fill the entire width."""
        for tab in self.tabs:
            tab.pack_forget()

        tab_width = self.root.winfo_width() // len(self.tabs) if self.tabs else self.root.winfo_width()
        for tab in self.tabs:
            tab.pack(side='left', expand=True, fill='x')
            tab.config(width=tab_width)

    def undo(self, event=None):
        """Undo the last action in the current text area."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Undo>>")

    def redo(self, event=None):
        """Redo the last undone action in the current text area."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Redo>>")

    def cut(self, event=None):
        """Cut the selected text."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Cut>>")

    def copy(self, event=None):
        """Copy the selected text."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Copy>>")

    def paste(self, event=None):
        """Paste from the clipboard."""
        current_tab_index = self.get_current_tab_index()
        if current_tab_index is not None:
            self.text_areas[current_tab_index].event_generate("<<Paste>>")

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        self.theme = "dark" if self.theme == "light" else "light"
        for text_area in self.text_areas:
            self.apply_theme(text_area)
        self.update_tab_layout()

    def apply_theme(self, widget):
        """Apply the current theme to a widget."""
        if self.theme == "light":
            self.tab_frame.config(style='Light.TFrame')
            widget.config(bg="#f0f0f0", fg="#000000")
            self.root.config(bg="#d3d3d3")
            self.tab_frame.config(style='Light.TFrame')
        else:
            self.tab_frame.config(style='Dark.TFrame')
            widget.config(bg="#303030", fg="#ffffff")
            self.root.config(bg="#404040")
            self.tab_frame.config(style='Dark.TFrame')

    def change_font(self):
        """Open a dialog to change font and font size."""
        font_window = tk.Toplevel(self.root)
        font_window.title("Font Settings")

        # Font family selection
        ttk.Label(font_window, text="Font Family:").grid(row=0, column=0, padx=5, pady=5)
        font_family_var = tk.StringVar(value=self.font_family)
        font_family_combo = ttk.Combobox(font_window, textvariable=font_family_var, values=font.families())
        font_family_combo.grid(row=0, column=1, padx=5, pady=5)

        # Font size selection
        ttk.Label(font_window, text="Font Size:").grid(row=1, column=0, padx=5, pady=5)
        font_size_var = tk.IntVar(value=self.font_size)
        font_size_spin = ttk.Spinbox(font_window, from_=8, to=72, textvariable=font_size_var)
        font_size_spin.grid(row=1, column=1, padx=5, pady=5)

        # Apply button
        ttk.Button(font_window, text="Apply", command=lambda: self.apply_font(font_family_var.get(), font_size_var.get())).grid(row=2, column=0, columnspan=2, pady=10)

    def apply_font(self, family, size):
        """Apply the selected font to all text widgets."""
        self.font_family = family
        self.font_size = size
        for text_area in self.text_areas:
            text_area.config(font=(family, size))

if __name__ == "__main__":
    root = tk.Tk()
    
    app = TextEditor(root)
    root.mainloop()
