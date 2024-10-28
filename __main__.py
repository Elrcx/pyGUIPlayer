import ttkbootstrap as ttk
from player import setup_player
from ui import setup_ui
import state


def main():
    app = ttk.Window(themename="darkly")
    app.title("Music Player")
    app.geometry("550x600")
    app.grid_columnconfigure(0, weight=1)
    state.app = app

    setup_player()
    setup_ui()
    app.mainloop()

if __name__ == '__main__':
    main()
