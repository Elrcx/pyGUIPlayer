from mutagen import File
import os


def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def get_track_metadata(file_path):
    try:
        audio = File(file_path)

        if audio is not None and audio.info is not None:
            duration = int(audio.info.length)
        else:
            duration = 0

        artist = audio.get('TPE1', "?")
        album = audio.get('TALB', "?")
        title = audio.get('TIT2', os.path.basename(file_path))
        return duration, artist, album, title
    except Exception as e:
        print(f"Error with loading metadata from {file_path}: {e}")
        return 300, "?", "?", os.path.basename(file_path)
