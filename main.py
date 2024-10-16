import ttkbootstrap as ttk
from tkinter import filedialog
import pygame
import os

mixer_volume = 100
song_length_in_s = 0
track_list = []
current_track_index = 0

current_song_time = 0
is_timer_running = False

user_dragging_progress_slider = False
progress_update_job = None

pygame.mixer.init()

def format_time(seconds):
    mins = seconds // 60
    secs = seconds % 60
    return f"{mins:02}:{secs:02}"

def load_music():
    global song_length_in_s, current_song_time, is_timer_running, progress_update_job, current_track_index
    file_paths = filedialog.askopenfilenames(
        filetypes=[("MP3 Files", "*.mp3"), ("WAV Files", "*.wav"), ("All Files", "*.*")])
    if file_paths:
        for file_path in file_paths:
            track_list.append(file_path)
            file_name = os.path.basename(file_path)
            track_table.insert('', 'end', values=(len(track_list), file_name, '', ''))

    if len(track_list) > 0:
        current_track_index = 0
        play_track(current_track_index)

def play_track(index):
    global song_length_in_s, current_song_time, is_timer_running, progress_update_job
    file_path = track_list[index]

    if progress_update_job is not None:
        app.after_cancel(progress_update_job)

    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    song_length_in_s = 300  # Example length, you can replace it with actual song length logic
    song_progress_slider.config(to=song_length_in_s)
    max_time_label.config(text=f"/ {format_time(song_length_in_s)}")
    current_song_time = 0
    is_timer_running = True
    update_progress_slider()

    file_name = os.path.basename(file_path)
    track_name_label.config(text=file_name)

def pause_music():
    global is_timer_running
    if is_timer_running:
        pygame.mixer.music.pause()
        is_timer_running = False
        pause_button.config(text="▶")
    else:
        pygame.mixer.music.unpause()
        is_timer_running = True
        pause_button.config(text="⏸︎")

def stop_music():
    global current_song_time, is_timer_running, progress_update_job
    pygame.mixer.music.stop()
    current_time_label.config(text=format_time(0))
    current_song_time = 0
    is_timer_running = False
    if progress_update_job is not None:
        app.after_cancel(progress_update_job)

def set_volume(event):
    volume = volume_slider.get() / 100
    pygame.mixer.music.set_volume(volume)

def update_progress_slider():
    global current_song_time, progress_update_job
    if is_timer_running and not user_dragging_progress_slider:
        current_song_time += 1
        if current_song_time <= song_length_in_s:
            song_progress_slider.set(current_song_time)
            current_time_label.config(text=format_time(current_song_time))
    progress_update_job = app.after(1000, update_progress_slider)

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
app.geometry("500x600")

track_name_label = ttk.Label(app, text="Track Name")
track_name_label.pack(pady=5)

main_frame = ttk.Frame(app)
main_frame.pack(fill="x", padx=10, pady=5)

song_progress_slider = ttk.Scale(main_frame, from_=0, to=100, length=400)
song_progress_slider.pack(side="left", fill="x", expand=True)
song_progress_slider.bind("<Button-1>", on_progress_slider_press)
song_progress_slider.bind("<ButtonRelease-1>", on_progress_slider_release)

controls_frame = ttk.Frame(app)
controls_frame.pack(fill="x", pady=10)

control_buttons_frame = ttk.Frame(controls_frame)
control_buttons_frame.pack(side="left", padx=10)

skip_back_button = ttk.Button(control_buttons_frame, text="⏮︎︎")
skip_back_button.pack(side="left", padx=5)

stop_button = ttk.Button(control_buttons_frame, text="⏹︎", command=stop_music)
stop_button.pack(side="left", padx=5)

pause_button = ttk.Button(control_buttons_frame, text="⏸︎", command=pause_music)
pause_button.pack(side="left", padx=5)

skip_forward_button = ttk.Button(control_buttons_frame, text="⏭︎")
skip_forward_button.pack(side="left", padx=5)

time_frame = ttk.Frame(controls_frame)
time_frame.pack(side="right", padx=10)

volume_frame = ttk.Frame(time_frame)
volume_frame.pack(side="left", padx=10, pady=10, fill="x")

volume_slider = ttk.Scale(volume_frame, from_=0, to=100, orient='horizontal', value=mixer_volume, command=set_volume)
volume_slider.pack()
set_volume(None)

current_time_label = ttk.Label(time_frame, text="00:00")
current_time_label.pack(side="left")

max_time_label = ttk.Label(time_frame, text="/ 00:00")
max_time_label.pack(side="left")

load_button = ttk.Button(app, text="Play from file", command=load_music)
load_button.pack(pady=10)

track_table = ttk.Treeview(app, columns=('Number', 'Title', 'Artist/Album', 'Duration'), show='headings', height=10)
track_table.heading('Number', text='#')
track_table.heading('Title', text='Title')
track_table.heading('Artist/Album', text='Artist/Album')
track_table.heading('Duration', text='Duration')
track_table.column('Number', width=30, stretch=False)
track_table.column('Title', width=200, stretch=True)
track_table.column('Artist/Album', width=150)
track_table.column('Duration', width=80, stretch=False)

track_table.pack(fill="both", padx=10, pady=5)

app.mainloop()