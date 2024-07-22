import tkinter as tk
from settings import SettingsPage
from tkinter import filedialog, messagebox
from pathlib import Path
import yt_dlp
from tkinter import ttk
import configparser
import subprocess

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("FM 5.0")

        # Load settings from the configuration file
        self.load_settings()

        # Default download folder
        self.download_folder = Path(self.default_folder)

        # Create the download folder if it doesn't exist
        self.download_folder.mkdir(exist_ok=True)

        # GUI elements
        self.directions_label = tk.Label(root, text="Enter a valid YouTube URL:")
        self.directions_label.pack(pady=(10, 0))

        self.url_entry = tk.Entry(root, width=40)
        self.url_entry.pack(pady=(5, 10))

        self.download_button_mp4 = tk.Button(root, text="Download Video (MP4)", command=lambda: self.download_media('mp4'))
        self.download_button_mp4.pack(pady=5)

        self.download_button_mp3 = tk.Button(root, text="Download Audio (MP3)", command=lambda: self.download_media('mp3'))
        self.download_button_mp3.pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
        self.progress.pack(pady=5)

        # Listbox to display downloaded files
        self.download_listbox = tk.Listbox(root, selectmode=tk.SINGLE, height=5, width=50)
        self.download_listbox.pack(pady=10, padx=10)

        # Bind the <<ListboxSelect>> event to a callback function
        self.download_listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Button for deleting songs
        self.delete_button = tk.Button(root, text="Delete Song", command=self.delete_selected)
        self.delete_button.pack(pady=5)

        # Button for fetching contents
        self.fetch_button = tk.Button(root, text="Fetch Contents", command=self.fetch_contents)
        self.fetch_button.pack(pady=5)

        # Settings button
        self.settings_button = tk.Button(root, text="Settings", command=self.open_settings)
        self.settings_button.pack(pady=10)

        # Check if dark mode is enabled
        if self.dark_mode:
            self.apply_dark_mode()

        # Load the list of downloads
        self.load_downloads()

    def apply_dark_mode(self):
        # Apply dark mode color scheme to your widgets
        self.root.configure(bg='#2C2C2C')
        self.directions_label.configure(bg='#2C2C2C', fg='white')
        self.url_entry.configure(bg='#4D4D4D', fg='white')
        self.download_button_mp4.configure(bg='#007BFF', fg='white')
        self.download_button_mp3.configure(bg='#007BFF', fg='white')
        self.progress.configure(style='dark.Horizontal.TProgressbar')
        self.download_listbox.configure(bg='#4D4D4D', fg='white')
        self.delete_button.configure(bg='#DC3545', fg='white')
        self.fetch_button.configure(bg='#28A745', fg='white')
        self.settings_button.configure(bg='#6C757D', fg='white')

    def load_settings(self):
        # Load settings from the configuration file
        config = configparser.ConfigParser()
        config.read("settings.ini")

        # Update settings in the YoutubeDownloader instance
        self.default_folder = config.get('Settings', 'DefaultFolder', fallback='FM5')
        self.dark_mode = config.getboolean('Settings', 'DarkMode', fallback=False)

        # Update the download folder based on the new settings
        self.download_folder = Path(self.default_folder)
        self.download_folder.mkdir(exist_ok=True)

    def open_settings(self):
        # Create an instance of the SettingsPage when the settings button is clicked
        settings_root = tk.Toplevel(self.root)
        settings_page = SettingsPage(settings_root, self)

    def download_media(self, format):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'outtmpl': f'{self.download_folder}/%(title)s.%(ext)s',
            'progress_hooks': [self.update_progress],
        }

        if format == 'mp3':
            ydl_opts['format'] = 'bestaudio/best'
            ydl_opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }]

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info_dict = ydl.extract_info(url, download=True)
                title = info_dict.get('title', 'media')
                messagebox.showinfo("Success", f"{format.upper()} download completed successfully.")
                # Update the list of downloads
                self.load_downloads()
            except yt_dlp.DownloadError as e:
                messagebox.showerror("Error", f"Download failed: {e}")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            # Update progress bar
            progress_str = d['_percent_str'].strip('%')
            try:
                progress_value = float(progress_str)
                self.progress['value'] = progress_value
                self.progress.update_idletasks()
            except ValueError:
                pass  # Ignore if the conversion to float fails

    def load_downloads(self):
        # Clear existing items
        self.download_listbox.delete(0, tk.END)
        # List all files in the download folder
        for file in self.download_folder.iterdir():
            if file.is_file():
                self.download_listbox.insert(tk.END, file.name)

    def delete_selected(self):
        selected_index = self.download_listbox.curselection()
        if selected_index:
            selected_file = self.download_listbox.get(selected_index)
            selected_path = self.download_folder / selected_file
            # Ask for confirmation before deleting
            confirm = messagebox.askyesno("Confirm Deletion", f"Do you want to delete {selected_file}?")
            if confirm:
                selected_path.unlink()
                # Update the list of downloads
                self.load_downloads()

    def fetch_contents(self):
        # Fetch contents of the download folder
        self.load_downloads()

    def on_listbox_select(self, event):
        selected_index = self.download_listbox.curselection()
        if selected_index:
            selected_file = self.download_listbox.get(selected_index)
            selected_path = self.download_folder / selected_file

            # Open the file with the default media player
            try:
                subprocess.run([selected_path], shell=True)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()
