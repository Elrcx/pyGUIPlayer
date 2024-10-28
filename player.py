import pygame
from utils import format_time, get_track_metadata
from playlist import reformat_playlist_display
import state


def setup_player():
    pygame.mixer.init()
    state.play_track = play_track
    check_for_next_track()

def check_for_next_track():
    if not pygame.mixer.music.get_busy() and state.current_track_index is not None and state.is_timer_running:
        change_track(1)
    state.app.after(500, check_for_next_track)

def play_track(index):
    try:
        state.current_track_index = index
        file_path = state.track_list[index]

        if state.progress_update_job != '':
            state.app.after_cancel(state.progress_update_job)

        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        duration, artist, album, title = get_track_metadata(file_path)

        state.song_length_in_s = duration
        state.song_progress_slider.config(to=state.song_length_in_s)
        state.max_time_label.config(text=f"/ {format_time(state.song_length_in_s)}")
        state.current_song_time = 0
        state.is_timer_running = True
        update_progress_slider()

        state.track_name_label.config(text=title)
        reformat_playlist_display()
    except Exception as e:
        print(f"Error playing track {index}: {e}")
        stop_music()
    update_pause_button_text()

def change_track(direction):
    try:
        state.current_track_index += direction
        if state.current_track_index >= len(state.track_list):
            state.current_track_index = 0
        elif state.current_track_index < 0:
            state.current_track_index = len(state.track_list) - 1
        play_track(state.current_track_index)
    except IndexError:
        print("Track index out of range")
    except Exception as e:
        print(f"Error changing track {state.current_track_index}: {e}")

def pause_music():
    if state.is_timer_running:
        pygame.mixer.music.pause()
        state.is_timer_running = False
    else:
        pygame.mixer.music.unpause()
        state.is_timer_running = True
    update_pause_button_text()

def update_pause_button_text():
    if state.is_timer_running:
        state.pause_button.config(text="⏸")
    else:
        state.pause_button.config(text="▶")

def stop_music():
    state.is_timer_running = False
    pygame.mixer.music.rewind()
    pygame.mixer.music.set_pos(0)
    pygame.mixer.music.pause()
    state.current_time_label.config(text=format_time(0))
    state.current_song_time = 0
    state.song_progress_slider.set(state.current_song_time)

    if state.progress_update_job != '':
        state.app.after_cancel(state.progress_update_job)

    update_pause_button_text()

def set_volume(_):
    volume = state.volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)

def update_progress_slider():
    if state.is_timer_running and not state.user_dragging_progress_slider:
        state.current_song_time += 1
        if state.current_song_time <= state.song_length_in_s:
            state.song_progress_slider.set(state.current_song_time)
            state.current_time_label.config(text=format_time(state.current_song_time))
    state.progress_update_job = state.app.after(1000, update_progress_slider)

def on_progress_slider_press(_):
    state.user_dragging_progress_slider = True

def on_progress_slider_release(_):
    state.user_dragging_progress_slider = False
    state.current_song_time = int(state.song_progress_slider.get())
    pygame.mixer.music.set_pos(state.current_song_time)
    state.current_time_label.config(text=format_time(state.current_song_time))
