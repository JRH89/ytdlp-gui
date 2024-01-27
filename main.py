import tkinter as tk
from tkinter import filedialog, messagebox
from pathlib import Path
import yt_dlp
from tkinter import ttk

class YoutubeDownloader:
    def __init__(self, root):
        self.root = root
        self.root.title("FM 5.0")

        # Default download folder
        self.download_folder = Path('FM5')

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
        self.download_listbox.pack(pady=10)

        # Button for deleting songs
        self.delete_button = tk.Button(root, text="Delete Song", command=self.delete_selected)
        self.delete_button.pack(pady=5)

        # Button for fetching contents
        self.fetch_button = tk.Button(root, text="Fetch Contents", command=self.fetch_contents)
        self.fetch_button.pack(pady=5)

        # Load the list of downloads
        self.load_downloads()

    def download_media(self, format):
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Error", "Please enter a YouTube URL.")
            return

        ext = 'mp4' if format == 'mp4' else 'mp3'

        ydl_opts = {
            'format': 'bestvideo[ext={0}]+bestaudio[ext={0}]/best[ext={0}]'.format(ext),
            'outtmpl': f'{self.download_folder}/%(title)s.%(ext)s',
            'progress_hooks': [self.update_progress],
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                messagebox.showinfo("Success", f"{format.upper()} download completed successfully.")
                # Update the list of downloads
                self.load_downloads()
            except yt_dlp.DownloadError as e:
                messagebox.showerror("Error", f"Download failed: {e}")

    def update_progress(self, d):
        if d['status'] == 'downloading':
            # Update progress bar
            self.progress['value'] = d['_percent_str']
            self.progress.update_idletasks()

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

if __name__ == "__main__":
    root = tk.Tk()
    app = YoutubeDownloader(root)
    root.mainloop()
