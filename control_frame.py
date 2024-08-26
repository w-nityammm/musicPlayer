import customtkinter
import pygame
from PIL import Image, ImageTk
import random

class ControlFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)
        self.grid_columnconfigure(4, weight=0)
        self.grid_columnconfigure(5, weight=1)
        self.grid_columnconfigure(6, weight=0)
        self.grid_columnconfigure(7, weight=0)
        self.grid_columnconfigure(8, weight=0)

        # Load and resize images
        self.prev_image = Image.open("assets/previous.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.prev_image = ImageTk.PhotoImage(self.prev_image)

        self.play_image = Image.open("assets/play.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.play_image = ImageTk.PhotoImage(self.play_image)

        self.pause_image = Image.open("assets/pause.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.pause_image = ImageTk.PhotoImage(self.pause_image)

        self.next_image = Image.open("assets/next.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.next_image = ImageTk.PhotoImage(self.next_image)

        self.volume_image = Image.open("assets/volume (2).png").resize((20, 20), Image.Resampling.LANCZOS)
        self.volume_image = ImageTk.PhotoImage(self.volume_image)

        self.muted_volume_image = Image.open("assets/volume.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.muted_volume_image = ImageTk.PhotoImage(self.muted_volume_image)

        self.shuffle_image = Image.open("assets/shuffle.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.shuffle_image = ImageTk.PhotoImage(self.shuffle_image)

        self.shuffle1_image = Image.open("assets/shuffle1.png").resize((20, 20), Image.Resampling.LANCZOS)
        self.shuffle1_image = ImageTk.PhotoImage(self.shuffle1_image)

        self.shuffle_button = customtkinter.CTkButton(self, image=self.shuffle_image, text="", width=30, height=30, fg_color="#2b2b2b", command=self.toggle_shuffle)
        self.shuffle_button.grid(row=0, column=1, padx=(0, 1), pady=5)

        self.prev_button = customtkinter.CTkButton(self, image=self.prev_image, text="", width=30, height=30, fg_color="#2b2b2b", command=self.play_prev_song)
        self.prev_button.grid(row=0, column=2, padx=(0, 1), pady=5)

        self.play_pause_button = customtkinter.CTkButton(self, image=self.play_image, text="", width=30, height=30, fg_color="#2b2b2b", command=self.toggle_play_pause)
        self.play_pause_button.grid(row=0, column=3, padx=1, pady=5)

        self.next_button = customtkinter.CTkButton(self, image=self.next_image, text="", width=30, height=30, fg_color="#2b2b2b", command=self.play_next_song)
        self.next_button.grid(row=0, column=4, padx=(1, 0), pady=5)

        self.volume_button = customtkinter.CTkButton(self, image=self.volume_image, text="", width=30, height=30, fg_color="#2b2b2b", command=self.toggle_volume)
        self.volume_button.grid(row=0, column=6, padx=(10, 1), pady=5)

        self.volume_slider = customtkinter.CTkSlider(self, from_=0, to=1, command=self.set_volume, width=100)
        self.volume_slider.set(0.5)
        self.volume_slider.grid(row=0, column=7, padx=(1, 10), pady=5)

        self.is_playing = False
        self.is_muted = False
        self.is_shuffled = False
        self.previous_volume = 0.5

        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        self.master.after(100, self.check_pygame_events)

    def toggle_play_pause(self):
        if self.is_playing:
            self.pause_song()
        else:
            self.play_song()

    def play_song(self):
        pygame.mixer.music.unpause()
        self.play_pause_button.configure(image=self.pause_image)
        self.is_playing = True

    def pause_song(self):
        pygame.mixer.music.pause()
        self.play_pause_button.configure(image=self.play_image)
        self.is_playing = False

    def play_next_song(self):
        if self.is_shuffled:
            self.master.scrollable_checkbox_frame.play_random_song()
        else:
            self.master.scrollable_checkbox_frame.play_next_song()

    def play_prev_song(self):
        self.master.scrollable_checkbox_frame.play_prev_song()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(float(volume))

    def toggle_volume(self):
        if self.is_muted:
            self.volume_slider.set(self.previous_volume)
            pygame.mixer.music.set_volume(self.previous_volume)
            self.volume_button.configure(image=self.volume_image)
        else:
            self.previous_volume = self.volume_slider.get()
            self.volume_slider.set(0)
            pygame.mixer.music.set_volume(0)
            self.volume_button.configure(image=self.muted_volume_image)
        self.is_muted = not self.is_muted

    def toggle_shuffle(self):
        if self.is_shuffled:
            self.shuffle_button.configure(image=self.shuffle_image)
        else:
            self.shuffle_button.configure(image=self.shuffle1_image)
        self.is_shuffled = not self.is_shuffled

    def play_next_or_random_song(self):
        if self.is_shuffled:
            self.master.scrollable_checkbox_frame.play_random_song()
        else:
            self.master.scrollable_checkbox_frame.play_next_song()

    def check_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                self.play_next_or_random_song()
        self.master.after(100, self.check_pygame_events)