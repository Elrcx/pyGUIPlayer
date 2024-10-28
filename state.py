# UI components
song_progress_slider = None
track_name_label = None
track_table = None
current_time_label = None
max_time_label = None
pause_button = None
volume_slider = None

# Player
current_track_index = 0
song_length_in_s = 0
current_song_time = 0
is_timer_running = False
user_dragging_progress_slider = False
progress_update_job = ''

# Playlist
track_list = []

# References
app = None
play_track = None