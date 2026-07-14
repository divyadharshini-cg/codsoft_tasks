# app.py
"""Main application class that sets up the CustomTkinter root and manages navigation between screens.
"""
import os
import customtkinter as ctk
from constants import BACKGROUND_COLOR, CARD_COLOR, ICON_PATH, FONT_FAMILY
from ui import HomeScreen, GameScreen, SettingsScreen, StatsScreen

class TicTacToeApp:
    def __init__(self):
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("green")  # we will override colors per widget
        self.root = ctk.CTk()
        self.root.title("Tic‑Tac‑Toe AI")
        self.root.geometry("900x650")
        self.root.configure(fg_color=BACKGROUND_COLOR)
        # set window icon if available
        if os.path.exists(ICON_PATH):
            try:
                self.root.iconbitmap(ICON_PATH)
            except Exception:
                # CTk on Windows may not support .png icons via iconbitmap, ignore
                pass
        # container for frames
        self.container = ctk.CTkFrame(self.root, fg_color=BACKGROUND_COLOR)
        self.container.pack(fill="both", expand=True)
        self.frames = {}
        self._init_frames()
        self.show_frame("Home")

    def _init_frames(self):
        self.frames["Home"] = HomeScreen(parent=self.container, controller=self)
        self.frames["Game"] = GameScreen(parent=self.container, controller=self)
        self.frames["Settings"] = SettingsScreen(parent=self.container, controller=self)
        self.frames["Stats"] = StatsScreen(parent=self.container, controller=self)
        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

    def show_frame(self, name: str, **kwargs):
        """Raise the requested frame. Additional kwargs are passed to the frame's ``on_show`` method if it exists."""
        frame = self.frames[name]
        frame.tkraise()
        if hasattr(frame, "on_show"):
            frame.on_show(**kwargs)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    TicTacToeApp().run()
