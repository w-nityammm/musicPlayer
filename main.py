from control_frame import ControlFrame
from library_frame import Library

import customtkinter
import os
import pygame
from tkinter import filedialog, Menu, simpledialog
import random

class allSongs(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title, control_frame):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.add_songs_button = customtkinter.CTkButton(self, text="Add songs", command=self.add_songs)
        self.add_songs_button.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="ew")

        self.song_buttons = []
        self.song_file = "songs.txt"
        self.control_frame = control_frame

        pygame.init()
        pygame.mixer.init()

        self.load_songs()
        self.played_songs = set()

    def load_songs(self):
        if os.path.exists(self.song_file):
            with open(self.song_file, 'r', encoding='utf-8') as f:
                for line in f:
                    self.create_song_button(line.strip())

    def add_songs(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("MP3 files", "*.mp3")])
        if file_paths:
            with open(self.song_file, 'a', encoding='utf-8') as f:
                for file_path in file_paths:
                    f.write(file_path + '\n')
                    self.create_song_button(file_path)

    def create_song_button(self, file_path):
        song_name = os.path.basename(file_path).replace('.mp3', '')
        pady_value = (10, 0) if len(self.song_buttons) == 0 else (0, 0)
        button = customtkinter.CTkButton(self, text=song_name, command=lambda: self.play_song(file_path))
        button.grid(row=len(self.song_buttons) + 2, column=0, padx=10, pady=pady_value, sticky="ew")
        button.bind("<Button-3>", lambda event, path=file_path: self.show_context_menu(event, path))
        self.song_buttons.append(button)

    def show_context_menu(self, event, file_path):
        context_menu = Menu(self, tearoff=0)
        context_menu.add_command(label="Remove song", command=lambda: self.remove_song(file_path))
        context_menu.add_command(label="Rename song", command=lambda: self.rename_song(file_path))
        context_menu.tk_popup(event.x_root, event.y_root)

    def remove_song(self, file_path):
        if pygame.mixer.music.get_busy() and self.get_song_index(file_path) == self.current_song_index:
            pygame.mixer.music.stop()
        with open(self.song_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(self.song_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() != file_path:
                    f.write(line)
        for button in self.song_buttons:
            if button.cget("command").__closure__[0].cell_contents == file_path:
                button.destroy()
                self.song_buttons.remove(button)
                break

    def rename_song(self, file_path):
        new_name = simpledialog.askstring("Rename song", "Enter new name:")
        if new_name:
            new_file_path = os.path.join(os.path.dirname(file_path), new_name + '.mp3')
            os.rename(file_path, new_file_path)
            with open(self.song_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            with open(self.song_file, 'w', encoding='utf-8') as f:
                for line in lines:
                    if line.strip() == file_path:
                        f.write(new_file_path + '\n')
                    else:
                        f.write(line)
            for button in self.song_buttons:
                if button.cget("command").__closure__[0].cell_contents == file_path:
                    button.configure(text=new_name)
                    button.configure(command=lambda: self.play_song(new_file_path))
                    button.bind("<Button-3>", lambda event, path=new_file_path: self.show_context_menu(event, path))
                    break

    def play_song(self, file_path=None):
        if file_path:
            self.current_song_index = self.get_song_index(file_path)
        else:
            file_path = self.song_buttons[self.current_song_index].cget("command").__closure__[0].cell_contents
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        self.control_frame.play_song()
        self.played_songs.add(file_path)

    def get_song_index(self, file_path):
        for index, button in enumerate(self.song_buttons):
            if button.cget("command").__closure__[0].cell_contents == file_path:
                return index
        return -1

    def play_next_song(self):
        if self.current_song_index < len(self.song_buttons) - 1:
            self.current_song_index += 1
            self.play_song()

    def play_prev_song(self):
        if self.current_song_index > 0:
            self.current_song_index -= 1
            self.play_song()

    def play_random_song(self):
        remaining_songs = [button.cget("command").__closure__[0].cell_contents for button in self.song_buttons if button.cget("command").__closure__[0].cell_contents not in self.played_songs]
        if not remaining_songs:
            self.played_songs.clear()
            remaining_songs = [button.cget("command").__closure__[0].cell_contents for button in self.song_buttons]
        random_song = random.choice(remaining_songs)
        self.current_song_index = self.get_song_index(random_song)
        self.play_song(random_song)

    def rename_song(self, file_path):
        RenameWindow(self, file_path, self.perform_rename)

    def perform_rename(self, file_path, new_name):
        new_file_path = os.path.join(os.path.dirname(file_path), new_name + '.mp3')
        os.rename(file_path, new_file_path)
        with open(self.song_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        with open(self.song_file, 'w', encoding='utf-8') as f:
            for line in lines:
                if line.strip() == file_path:
                    f.write(new_file_path + '\n')
                else:
                    f.write(line)
        for button in self.song_buttons:
            if button.cget("command").__closure__[0].cell_contents == file_path:
                button.configure(text=new_name)
                button.configure(command=lambda: self.play_song(new_file_path))
                button.bind("<Button-3>", lambda event, path=new_file_path: self.show_context_menu(event, path))
                break

class RenameWindow(customtkinter.CTkToplevel):
    def __init__(self, master, file_path, rename_callback):
        super().__init__(master)
        self.file_path = file_path
        self.rename_callback = rename_callback

        self.geometry("300x150")
        self.overrideredirect(True)

        self.entry = customtkinter.CTkEntry(self, placeholder_text="Enter new name")
        self.entry.pack(pady=10, padx=10, fill="x")

        self.rename_button = customtkinter.CTkButton(self, text="Rename", command=self.rename_song)
        self.rename_button.pack(pady=10)

        self.close_button = customtkinter.CTkButton(self, text="Close", command=self.destroy)
        self.close_button.pack(pady=10)

    def rename_song(self):
        new_name = self.entry.get()
        if new_name:
            self.rename_callback(self.file_path, new_name)
            self.destroy()
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Musync")
        self.geometry("1200x600")
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        self.control_frame = ControlFrame(self)
        self.control_frame.grid(row=1, column=0, columnspan=2, padx=10, pady=(10, 0), sticky="nsew")
        self.control_frame.configure(height=100)

        self.scrollable_checkbox_frame = allSongs(self, title="All songs", control_frame=self.control_frame)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.scrollable_radiobutton_frame = Library(self, title="Youtube Download", all_songs_frame=self.scrollable_checkbox_frame)
        self.scrollable_radiobutton_frame.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nsew")

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def on_closing(self):
        self.scrollable_checkbox_frame.delete_marked_songs()
        self.destroy()

app = App()
app.mainloop()