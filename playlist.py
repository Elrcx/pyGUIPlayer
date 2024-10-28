from tkinter import filedialog
from utils import format_time, get_track_metadata
import state


def on_track_double_click(_):
    selected_item = state.track_table.selection()[0]

    if selected_item:
        track_number = int(state.track_table.item(selected_item)['values'][1]) - 1
        state.play_track(track_number)

def clear_playlist():
    state.track_list.clear()
    for item in state.track_table.get_children():
        state.track_table.delete(item)

def delete_selected_track(_):
    try:
        selected_item = state.track_table.selection()[0]

        if selected_item:
            track_number = int(state.track_table.item(selected_item)['values'][1]) - 1
            del state.track_list[track_number]

            if track_number < state.current_track_index:
                state.current_track_index -= 1
            elif track_number == state.current_track_index:
                state.current_track_index = None

            state.track_table.delete(selected_item)
            reformat_playlist_display()
    except IndexError:
        print("No track selected to delete.")
    except Exception as e:
        print(f"Error deleting selected track: {e}")

def save_playlist():
    try:
        playlist_file = filedialog.asksaveasfilename(defaultextension=".playlist", filetypes=[("Playlist Files", "*.playlist")])

        if playlist_file:
            with open(playlist_file, 'w') as file:
                for track in state.track_list:
                    file.write(track + "\n")
    except Exception as e:
        print(f"Error saving playlist: {e}")

def load_playlist():
    try:
        playlist_file = filedialog.askopenfilename(filetypes=[("Playlist Files", "*.playlist")])

        if playlist_file:
            with open(playlist_file, 'r') as file:
                for line in file:
                    track_path = line.strip()
                    add_entry_to_playlist(track_path)

            if len(state.track_list) > 0:
                state.current_track_index = 0
                state.play_track(state.current_track_index)
    except Exception as e:
        print(f"Error loading playlist: {e}")

def add_entry_to_playlist(file_path):
    state.track_list.append(file_path)
    duration, artist, album, title = get_track_metadata(file_path)
    state.track_table.insert('', 'end', values=('', len(state.track_list), title, f"{artist} - {album}", format_time(duration)))
    reformat_playlist_display()

def load_music():
    try:
        file_paths = filedialog.askopenfilenames(
            filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")]
        )
        if file_paths:
            for file_path in file_paths:
                add_entry_to_playlist(file_path)

        if len(state.track_list) > 0:
            state.current_track_index = 0
            state.play_track(state.current_track_index)
    except Exception as e:
        print(f"Error loading music files: {e}")

def reformat_playlist_display():
    item_ids = state.track_table.get_children()
    for i, item_id in enumerate(item_ids):
        if i == state.current_track_index:
            state.track_table.item(item_id, values=('▶', i + 1,
                                                    state.track_table.item(item_id, 'values')[2],
                                                    state.track_table.item(item_id, 'values')[3],
                                                    state.track_table.item(item_id, 'values')[4]))
        else:
            state.track_table.item(item_id, values=('', i + 1,
                                                    state.track_table.item(item_id, 'values')[2],
                                                    state.track_table.item(item_id, 'values')[3],
                                                    state.track_table.item(item_id, 'values')[4]))
