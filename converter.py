### converter.py
# A simple GUI application to convert Spotify playlists to Rekordbox M3U format.
# 1. Eventually to be an all in one rekordbox soulseek helper - allowing for one to take a spotify playlist, download the tracks from soulseek, and then export to rekordbox.
# 2. Using beets to manage songs downloaded from soulseek playlists will maintain consistent data (not as important as step 1)

import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox


class PlaylistGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Spotify to Rekordbox Playlist Converter")
        self.root.geometry("600x300")
        self.csv_path = None
        self.music_dir = None
        self.export_path = None

        # CSV selection
        tk.Button(
            root, text="Select Spotify CSV", width=40, command=self.select_csv
        ).pack(pady=(10, 0))
        self.csv_label = tk.Label(root, text="No file selected", fg="gray")
        self.csv_label.pack()

        # Music folder selection
        tk.Button(
            root, text="Select Music Directory", width=40, command=self.select_music_dir
        ).pack(pady=(10, 0))
        self.music_label = tk.Label(root, text="No folder selected", fg="gray")
        self.music_label.pack()

        # Export location selection
        tk.Button(
            root,
            text="Select Export Location",
            width=40,
            command=self.select_export_path,
        ).pack(pady=(10, 0))
        self.export_label = tk.Label(root, text="No export path selected", fg="gray")
        self.export_label.pack()

        # Generate button
        tk.Button(
            root, text="Generate M3U Playlist", width=40, command=self.generate_playlist
        ).pack(pady=20)

    def select_csv(self):
        path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if path:
            self.csv_path = path
            self.csv_label.config(text=path, fg="black")

    def select_music_dir(self):
        path = filedialog.askdirectory()
        if path:
            self.music_dir = path
            self.music_label.config(text=path, fg="black")

    def select_export_path(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".m3u", filetypes=[("M3U Playlist", "*.m3u")]
        )
        if path:
            self.export_path = path
            self.export_label.config(text=path, fg="black")

    def generate_playlist(self):
        if not all([self.csv_path, self.music_dir, self.export_path]):
            messagebox.showwarning(
                "Missing Info", "Please select all required files and directories."
            )
            return

        try:
            df = pd.read_csv(self.csv_path)
            m3u_lines = ["#EXTM3U"]

            for _, row in df.iterrows():
                track_name = row["Track Name"]
                artist = row["Artist Name(s)"]
                filename = f"{artist} - {track_name}.mp3"
                filepath = os.path.join(self.music_dir, filename)
                m3u_lines.append(f"#EXTINF:0,{artist} - {track_name}")
                m3u_lines.append(filepath)

            with open(self.export_path, "w", encoding="utf-8") as f:
                f.write("\n".join(m3u_lines))

            messagebox.showinfo("Success", f"Playlist saved to:\n{self.export_path}")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistGenerator(root)
    root.mainloop()
