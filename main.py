import ttkbootstrap as ttk
from tkinter import filedialog
import pygame

mixer_volume = 100
song_length_in_s = 0

current_song_time = 0
is_timer_running = False

user_dragging_progress_slider = False

pygame.mixer.init()

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def load_music():
    global song_length_in_s, current_song_time, is_timer_running
    file_path = filedialog.askopenfilename(filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")])
    if file_path:
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()

        song_length_in_s = 300
        song_progress_slider.config(to=song_length_in_s)
        max_time_label.config(text=f"/ {format_time(song_length_in_s)}")
        current_song_time = 0
        is_timer_running = True
        update_progress_slider()

def pause_music():
    global is_timer_running
    pygame.mixer.music.pause()
    is_timer_running = False

def unpause_music():
    global is_timer_running
    pygame.mixer.music.unpause()
    is_timer_running = True

def stop_music():
    global current_song_time, is_timer_running
    pygame.mixer.music.stop()
    current_time_label.config(text=format_time(0))
    current_song_time = 0
    is_timer_running = False

def set_volume(event):
    volume = volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)

def update_progress_slider():
    global current_song_time
    if is_timer_running and not user_dragging_progress_slider:
        current_song_time += 1
        if current_song_time <= song_length_in_s:
            song_progress_slider.set(current_song_time)
            current_time_label.config(text=format_time(current_song_time))
    app.after(1000, update_progress_slider)

def on_progress_slider_press(event):
    global user_dragging_progress_slider
    user_dragging_progress_slider = True

def on_progress_slider_release(event):
    global user_dragging_progress_slider, current_song_time
    user_dragging_progress_slider = False

    current_song_time = int(song_progress_slider.get())
    pygame.mixer.music.pause()
    pygame.mixer.music.set_pos(current_song_time)
    current_time_label.config(text=format_time(current_song_time))
    pygame.mixer.music.unpause()


app = ttk.Window(themename="darkly")
app.title("Music Player")
app.geometry("400x300")

song_progress_slider = ttk.Scale(from_=0, to=100, length=200)
song_progress_slider.pack(pady=10)
song_progress_slider.bind("<Button-1>", on_progress_slider_press)
song_progress_slider.bind("<ButtonRelease-1>", on_progress_slider_release)

time_frame = ttk.Frame(app)
time_frame.pack(pady=5)

current_time_label = ttk.Label(time_frame, text="00:00")
current_time_label.pack(side="left")

max_time_label = ttk.Label(time_frame, text="/ 00:00")
max_time_label.pack(side="left")

load_button = ttk.Button(app, text="Play from file", command=load_music)
load_button.pack(pady=10)

pause_button = ttk.Button(app, text="Pause", command=pause_music)
pause_button.pack(pady=10)

unpause_button = ttk.Button(app, text="Unpause", command=unpause_music)
unpause_button.pack(pady=10)

stop_button = ttk.Button(app, text="Stop", command=stop_music)
stop_button.pack(pady=10)

volume_slider = ttk.Scale(from_=100, to=0, orient='vertical', value=mixer_volume, command=set_volume)
volume_slider.pack(pady=10)
set_volume(None)

app.mainloop()