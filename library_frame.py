import customtkinter
import yt_dlp
import os

class Library(customtkinter.CTkScrollableFrame):
    def __init__(self, master, title="Youtube Download", all_songs_frame=None):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = customtkinter.CTkLabel(self, text=title)
        self.title_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.link_entry = customtkinter.CTkEntry(self, placeholder_text="Enter link...")
        self.link_entry.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="ew")

        self.download_button = customtkinter.CTkButton(self, text="Download", corner_radius=10, height=50, width=200, font=("Arial", 16), command=self.download_mp3)
        self.download_button.grid(row=2, column=0, padx=10, pady=(30, 0))

        self.all_songs_frame = all_songs_frame

    def download_mp3(self):
        link = self.link_entry.get()
        if not link:
            return

        output_path = 'ytsongs'
        os.makedirs(output_path, exist_ok=True)
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-ar', '44100'
            ],
            'prefer_ffmpeg': True,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(link, download=True)
                new_file = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

                original_file = ydl.prepare_filename(info_dict)
                if os.path.exists(original_file):
                    os.remove(original_file)

            with open('songs.txt', 'a', encoding='utf-8') as f:
                f.write(new_file + '\n')

            if self.all_songs_frame:
                self.all_songs_frame.create_song_button(new_file)
        except Exception as e:
            print(f"An error occurred: {e}")