import pandas as pd
import os

# Load CSV from Spotify
df = pd.read_csv("spotify_playlist.csv")

# Path to your local music folder
music_dir = "C:/Users/Ethan/Music"

# Start M3U content
m3u_lines = ["#EXTM3U"]

for _, row in df.iterrows():
    track_name = row["Track Name"]
    artist = row["Artist"]
    filename = f"{artist} - {track_name}.mp3"
    filepath = os.path.join(music_dir, filename)
    m3u_lines.append(f"#EXTINF:0,{artist} - {track_name}")
    m3u_lines.append(filepath)

# Save M3U
with open("rekordbox_playlist.m3u", "w", encoding="utf-8") as f:
    f.write("\n".join(m3u_lines))
