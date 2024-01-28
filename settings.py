# settings.py

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import configparser

class SettingsPage:
    def __init__(self, root, youtube_downloader):
        self.root = root
        self.root.title("Settings")
        self.root.geometry("400x200")

        # Reference to the YoutubeDownloader instance
        self.youtube_downloader = youtube_downloader

        # Config file path
        self.config_file = 'settings.ini'

        # Dark mode checkbox
        self.dark_mode_var = tk.BooleanVar()
        self.dark_mode_var.set(self.youtube_downloader.dark_mode)
        self.dark_mode_checkbox = tk.Checkbutton(root, text="Dark Mode", variable=self.dark_mode_var)
        self.dark_mode_checkbox.pack(pady=10)

        # Default download folder entry
        self.default_folder_label = tk.Label(root, text="Default Download Folder:")
        self.default_folder_label.pack(pady=(10, 0))

        self.default_folder_entry = tk.Entry(root, width=30)
        self.default_folder_entry.insert(0, self.youtube_downloader.default_folder)
        self.default_folder_entry.pack(pady=5)

        # Save button
        self.save_button = tk.Button(root, text="Save", command=self.save_settings)
        self.save_button.pack(pady=10)

        # Load settings
        self.load_settings()

    def load_settings(self):
        # Load settings from the configuration file
        config = configparser.ConfigParser()
        config.read(self.config_file)

        # Update GUI elements with the loaded settings
        self.dark_mode_var.set(config.getboolean('Settings', 'DarkMode', fallback=False))
        self.default_folder_entry.delete(0, tk.END)
        self.default_folder_entry.insert(0, config.get('Settings', 'DefaultFolder', fallback='FM5'))

    def save_settings(self):
        # Save settings to the configuration file
        config = configparser.ConfigParser()
        config['Settings'] = {
            'DarkMode': str(self.dark_mode_var.get()),
            'DefaultFolder': self.default_folder_entry.get(),
        }

        with open(self.config_file, 'w') as configfile:
            config.write(configfile)

        # Update the settings in the YoutubeDownloader instance
        self.youtube_downloader.load_settings()

        # Close the settings window
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsPage(root, None)  # Pass None since we don't have a YoutubeDownloader instance in this context
    root.mainloop()
