# ui.py
"""User Interface screens for the Tic‑Tac‑Toe AI desktop application.
Provides HomeScreen, GameScreen, SettingsScreen, and StatsScreen frames using CustomTkinter.
"""
import os
import customtkinter as ctk
from PIL import Image
from typing import List, Dict, Any

from constants import (
    BACKGROUND_COLOR, CARD_COLOR, ACCENT_COLOR, SUCCESS_COLOR, DANGER_COLOR,
    TEXT_COLOR, SECONDARY_TEXT_COLOR, FONT_FAMILY, Difficulty, GameState,
    CLICK_SOUND, WIN_SOUND, LOSE_SOUND, DRAW_SOUND, SPLASH_PATH
)
from utils import load_stats, save_stats, play_sound, set_sound_enabled
from game import TicTacToeGame
from ai import get_ai_move
from settings import load_settings, save_settings

class HomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller
        
        # Load splash image as banner
        if os.path.exists(SPLASH_PATH):
            try:
                pil_img = Image.open(SPLASH_PATH)
                self.logo_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(300, 200))
                self.logo_label = ctk.CTkLabel(self, image=self.logo_img, text="")
                self.logo_label.pack(pady=(40, 10))
            except Exception as e:
                print(f"[UI] Failed to load splash: {e}")
        
        # Title
        self.title_label = ctk.CTkLabel(
            self,
            text="TIC-TAC-TOE AI",
            font=(FONT_FAMILY, 38, "bold"),
            text_color=TEXT_COLOR
        )
        self.title_label.pack(pady=10)
        
        # Subtitle / Configuration Preview
        self.config_preview = ctk.CTkLabel(
            self,
            text="Mode: Loading...",
            font=(FONT_FAMILY, 14),
            text_color=SECONDARY_TEXT_COLOR
        )
        self.config_preview.pack(pady=(0, 30))
        
        # Main Card for Buttons
        self.card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16, width=400, height=280)
        self.card.pack_propagate(False)
        self.card.pack(pady=10)
        
        # Buttons
        self.play_btn = ctk.CTkButton(
            self.card,
            text="Start Match",
            font=(FONT_FAMILY, 16, "bold"),
            fg_color=ACCENT_COLOR,
            hover_color="#2563EB",
            height=45,
            corner_radius=10,
            command=self.on_play_click
        )
        self.play_btn.pack(fill="x", padx=40, pady=(40, 15))
        
        self.settings_btn = ctk.CTkButton(
            self.card,
            text="Game Settings",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color="#334155",
            hover_color="#475569",
            height=45,
            corner_radius=10,
            command=lambda: self.controller.show_frame("Settings")
        )
        self.settings_btn.pack(fill="x", padx=40, pady=15)
        
        self.stats_btn = ctk.CTkButton(
            self.card,
            text="View Statistics",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color="#334155",
            hover_color="#475569",
            height=45,
            corner_radius=10,
            command=lambda: self.controller.show_frame("Stats")
        )
        self.stats_btn.pack(fill="x", padx=40, pady=15)
        
    def on_show(self, **kwargs):
        """Update configurations when the home screen is focused."""
        settings = load_settings()
        # Initialize sound settings on launch
        set_sound_enabled(settings.get("sound_enabled", True))
        
        mode = "Player vs AI" if settings.get("game_mode") == "vs_ai" else "Local Pass & Play"
        diff = settings.get("difficulty", "MEDIUM")
        symbol = settings.get("player_symbol", "X")
        
        if settings.get("game_mode") == "vs_ai":
            preview_text = f"Mode: {mode} ({diff}) | Playing as {symbol}"
        else:
            preview_text = f"Mode: {mode}"
            
        self.config_preview.configure(text=preview_text)
        
    def on_play_click(self):
        play_sound(CLICK_SOUND)
        self.controller.show_frame("Game")


class GameScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller
        self.game = TicTacToeGame()
        
        # Left side panel for Info & controls, Right side panel for the 3x3 Board
        self.left_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.left_panel.pack(side="left", fill="both", expand=True, padx=30, pady=30)
        
        self.right_panel = ctk.CTkFrame(self, fg_color="transparent")
        self.right_panel.pack(side="right", fill="both", expand=True, padx=30, pady=30)
        
        # --- Left Panel widgets ---
        self.title_label = ctk.CTkLabel(
            self.left_panel,
            text="TIC-TAC-TOE",
            font=(FONT_FAMILY, 28, "bold"),
            text_color=TEXT_COLOR
        )
        self.title_label.pack(anchor="w", pady=(20, 5))
        
        self.subtitle_label = ctk.CTkLabel(
            self.left_panel,
            text="Beat the unbeatable AI",
            font=(FONT_FAMILY, 14),
            text_color=SECONDARY_TEXT_COLOR
        )
        self.subtitle_label.pack(anchor="w", pady=(0, 30))
        
        # Card container for info
        self.info_card = ctk.CTkFrame(self.left_panel, fg_color=CARD_COLOR, corner_radius=12, height=180)
        self.info_card.pack_propagate(False)
        self.info_card.pack(fill="x", pady=10)
        
        # Status text inside info card
        self.status_label = ctk.CTkLabel(
            self.info_card,
            text="Your Turn (X)",
            font=(FONT_FAMILY, 20, "bold"),
            text_color=ACCENT_COLOR
        )
        self.status_label.pack(expand=True, fill="both", padx=20, pady=10)
        
        # Action Buttons
        self.restart_btn = ctk.CTkButton(
            self.left_panel,
            text="Restart Match",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color=ACCENT_COLOR,
            hover_color="#2563EB",
            height=45,
            corner_radius=10,
            command=self.start_game
        )
        self.restart_btn.pack(fill="x", pady=(20, 10))
        
        self.back_btn = ctk.CTkButton(
            self.left_panel,
            text="Back to Menu",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color="#334155",
            hover_color="#475569",
            height=45,
            corner_radius=10,
            command=self.go_back
        )
        self.back_btn.pack(fill="x", pady=10)
        
        # --- Right Panel (Grid Board) ---
        self.board_card = ctk.CTkFrame(self.right_panel, fg_color=CARD_COLOR, corner_radius=16, width=380, height=380)
        self.board_card.pack_propagate(False)
        self.board_card.pack(expand=True)
        
        self.grid_frame = ctk.CTkFrame(self.board_card, fg_color="transparent")
        self.grid_frame.pack(expand=True, padx=20, pady=20)
        
        self.buttons: List[ctk.CTkButton] = []
        for i in range(9):
            btn = ctk.CTkButton(
                self.grid_frame,
                text="",
                width=100,
                height=100,
                corner_radius=12,
                font=(FONT_FAMILY, 36, "bold"),
                fg_color=BACKGROUND_COLOR,
                hover_color="#1E293B",
                command=lambda idx=i: self.on_cell_click(idx)
            )
            row = i // 3
            col = i % 3
            btn.grid(row=row, column=col, padx=6, pady=6)
            self.buttons.append(btn)
            
        # State variables
        self.game_mode = "vs_ai"
        self.difficulty = Difficulty.MEDIUM
        self.player_symbol = "X"
        self.ai_symbol = "O"

    def on_show(self, **kwargs):
        """Prepares the game using selected preferences."""
        settings = load_settings()
        self.game_mode = settings.get("game_mode", "vs_ai")
        self.difficulty = Difficulty[settings.get("difficulty", "MEDIUM")]
        self.player_symbol = settings.get("player_symbol", "X")
        self.ai_symbol = "O" if self.player_symbol == "X" else "X"
        
        # Apply title subtitle
        if self.game_mode == "vs_ai":
            self.subtitle_label.configure(text=f"AI Difficulty: {self.difficulty.name}")
        else:
            self.subtitle_label.configure(text="Local Pass & Play Mode")
            
        self.start_game()

    def start_game(self):
        """Initializes a new match."""
        # Clean buttons
        for btn in self.buttons:
            btn.configure(
                text="",
                fg_color=BACKGROUND_COLOR,
                hover_color="#1E293B"
            )
        # Restart internal board
        # X always plays first
        self.game.reset(starting_player="X")
        self.update_ui_board()
        self.check_ai_turn()

    def on_cell_click(self, index: int):
        # Guard if it's the AI's turn
        if self.game_mode == "vs_ai" and self.game.current_player == self.ai_symbol:
            return
        if self.game.board[index] != "" or self.game.state != GameState.IN_PROGRESS:
            return
            
        self.game.make_move(index)
        play_sound(CLICK_SOUND)
        self.update_ui_board()
        
        if self.game.state != GameState.IN_PROGRESS:
            self.handle_game_over()
        else:
            self.check_ai_turn()

    def check_ai_turn(self):
        """Runs the AI search asynchronously if appropriate."""
        if self.game.state == GameState.IN_PROGRESS and self.game_mode == "vs_ai" and self.game.current_player == self.ai_symbol:
            self.status_label.configure(text="AI is thinking...", text_color=ACCENT_COLOR)
            # Disable board buttons temporarily
            for btn in self.buttons:
                btn.configure(hover_color=BACKGROUND_COLOR)
            # Artificial delay for premium feel
            self.after(500, self.make_ai_move)
        else:
            # Player turn
            self.update_status_label()

    def make_ai_move(self):
        """Calculates and executes AI's choice."""
        if self.game.state != GameState.IN_PROGRESS:
            return
        try:
            ai_move = get_ai_move(self.game, self.difficulty, self.ai_symbol)
            self.game.make_move(ai_move)
            play_sound(CLICK_SOUND)
            self.update_ui_board()
            
            if self.game.state != GameState.IN_PROGRESS:
                self.handle_game_over()
            else:
                self.update_status_label()
        except Exception as e:
            print(f"[Game] AI calculation error: {e}")

    def update_ui_board(self):
        """Renders current board array symbols onto buttons."""
        for i, val in enumerate(self.game.board):
            if val == "X":
                self.buttons[i].configure(
                    text="X",
                    fg_color=CARD_COLOR,
                    text_color=ACCENT_COLOR,
                    hover_color=CARD_COLOR
                )
            elif val == "O":
                self.buttons[i].configure(
                    text="O",
                    fg_color=CARD_COLOR,
                    text_color=DANGER_COLOR,
                    hover_color=CARD_COLOR
                )
            else:
                self.buttons[i].configure(
                    text="",
                    fg_color=BACKGROUND_COLOR,
                    hover_color="#1E293B"
                )

    def update_status_label(self):
        """Displays who is active currently."""
        curr = self.game.current_player
        if self.game_mode == "vs_ai":
            if curr == self.player_symbol:
                self.status_label.configure(text=f"Your Turn ({curr})", text_color=ACCENT_COLOR)
            else:
                self.status_label.configure(text="AI's Turn", text_color=DANGER_COLOR)
        else:
            self.status_label.configure(text=f"Player {curr}'s Turn", text_color=ACCENT_COLOR if curr == "X" else DANGER_COLOR)

    def handle_game_over(self):
        """Handles highlight styles, score persistence, and playbacks."""
        # Highlight winning cells
        if self.game.state in (GameState.X_WON, GameState.O_WON):
            for cell_idx in self.game.winner_cells:
                self.buttons[cell_idx].configure(
                    fg_color=SUCCESS_COLOR,
                    text_color="#FFFFFF",
                    hover_color=SUCCESS_COLOR
                )
                
        # Stats updates
        stats = load_stats()
        stats["games_played"] = stats.get("games_played", 0) + 1
        stats["total_moves"] = stats.get("total_moves", 0) + sum(1 for cell in self.game.board if cell != "")
        
        outcome = self.game.state
        if outcome == GameState.DRAW:
            stats["draws"] = stats.get("draws", 0) + 1
            play_sound(DRAW_SOUND)
            self.status_label.configure(text="It's a draw!", text_color=SECONDARY_TEXT_COLOR)
            stats["current_streak"] = 0
        else:
            winner = "X" if outcome == GameState.X_WON else "O"
            if self.game_mode == "vs_ai":
                if winner == self.player_symbol:
                    stats["wins"] = stats.get("wins", 0) + 1
                    stats["current_streak"] = stats.get("current_streak", 0) + 1
                    stats["longest_win_streak"] = max(stats.get("longest_win_streak", 0), stats["current_streak"])
                    play_sound(WIN_SOUND)
                    self.status_label.configure(text="You won! 🎉", text_color=SUCCESS_COLOR)
                else:
                    stats["losses"] = stats.get("losses", 0) + 1
                    stats["current_streak"] = 0
                    play_sound(LOSE_SOUND)
                    self.status_label.configure(text="AI won! 🤖", text_color=DANGER_COLOR)
            else:
                play_sound(WIN_SOUND)
                self.status_label.configure(text=f"Player {winner} Won!", text_color=SUCCESS_COLOR)
                
        save_stats(stats)

    def go_back(self):
        play_sound(CLICK_SOUND)
        self.controller.show_frame("Home")


class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller
        
        # Center container
        self.center_card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16, width=500, height=480)
        self.center_card.pack_propagate(False)
        self.center_card.pack(expand=True, pady=40)
        
        self.title_label = ctk.CTkLabel(
            self.center_card,
            text="SETTINGS",
            font=(FONT_FAMILY, 24, "bold"),
            text_color=TEXT_COLOR
        )
        self.title_label.pack(pady=(30, 20))
        
        # Game Mode
        self.mode_label = ctk.CTkLabel(self.center_card, text="Game Mode", font=(FONT_FAMILY, 14, "bold"), text_color=SECONDARY_TEXT_COLOR)
        self.mode_label.pack(anchor="w", padx=50, pady=(10, 2))
        self.mode_btn = ctk.CTkSegmentedButton(
            self.center_card,
            values=["vs_ai", "vs_player"],
            command=self.on_mode_change,
            height=35
        )
        self.mode_btn.pack(fill="x", padx=50, pady=(0, 15))
        
        # Difficulty
        self.diff_label = ctk.CTkLabel(self.center_card, text="AI Difficulty", font=(FONT_FAMILY, 14, "bold"), text_color=SECONDARY_TEXT_COLOR)
        self.diff_label.pack(anchor="w", padx=50, pady=(10, 2))
        self.diff_btn = ctk.CTkSegmentedButton(
            self.center_card,
            values=["EASY", "MEDIUM", "HARD", "EXPERT"],
            height=35
        )
        self.diff_btn.pack(fill="x", padx=50, pady=(0, 15))
        
        # Player Symbol
        self.sym_label = ctk.CTkLabel(self.center_card, text="Play Symbol (as P1)", font=(FONT_FAMILY, 14, "bold"), text_color=SECONDARY_TEXT_COLOR)
        self.sym_label.pack(anchor="w", padx=50, pady=(10, 2))
        self.sym_btn = ctk.CTkSegmentedButton(
            self.center_card,
            values=["X", "O"],
            height=35
        )
        self.sym_btn.pack(fill="x", padx=50, pady=(0, 20))
        
        # Sound Effects
        self.sound_switch = ctk.CTkSwitch(
            self.center_card,
            text="Sound Effects Enabled",
            font=(FONT_FAMILY, 14),
            progress_color=SUCCESS_COLOR
        )
        self.sound_switch.pack(anchor="w", padx=50, pady=10)
        
        # Bottom Button Frame
        self.btn_frame = ctk.CTkFrame(self.center_card, fg_color="transparent")
        self.btn_frame.pack(fill="x", side="bottom", pady=25)
        
        self.save_btn = ctk.CTkButton(
            self.btn_frame,
            text="Save Settings",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color=SUCCESS_COLOR,
            hover_color="#16A34A",
            height=40,
            command=self.save_settings
        )
        self.save_btn.pack(side="right", padx=50, expand=True, fill="x")
        
    def on_show(self, **kwargs):
        settings = load_settings()
        
        # Load mode
        mode = settings.get("game_mode", "vs_ai")
        self.mode_btn.set(mode)
        
        # Load diff
        diff = settings.get("difficulty", "MEDIUM")
        self.diff_btn.set(diff)
        
        # Load symbol
        sym = settings.get("player_symbol", "X")
        self.sym_btn.set(sym)
        
        # Sound
        snd = settings.get("sound_enabled", True)
        if snd:
            self.sound_switch.select()
        else:
            self.sound_switch.deselect()
            
        self.on_mode_change(mode)

    def on_mode_change(self, value):
        """Enables/Disables Difficulty & Symbol buttons based on Mode selection."""
        if value == "vs_player":
            self.diff_btn.configure(state="disabled")
            self.sym_btn.configure(state="disabled")
        else:
            self.diff_btn.configure(state="normal")
            self.sym_btn.configure(state="normal")

    def save_settings(self):
        settings = {
            "game_mode": self.mode_btn.get(),
            "difficulty": self.diff_btn.get(),
            "player_symbol": self.sym_btn.get(),
            "sound_enabled": bool(self.sound_switch.get())
        }
        save_settings(settings)
        set_sound_enabled(settings["sound_enabled"])
        
        play_sound(CLICK_SOUND)
        self.controller.show_frame("Home")


class StatsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BACKGROUND_COLOR)
        self.controller = controller
        
        # Center container
        self.center_card = ctk.CTkFrame(self, fg_color=CARD_COLOR, corner_radius=16, width=650, height=520)
        self.center_card.pack_propagate(False)
        self.center_card.pack(expand=True, pady=30)
        
        self.title_label = ctk.CTkLabel(
            self.center_card,
            text="STATISTICS & RECORDS",
            font=(FONT_FAMILY, 26, "bold"),
            text_color=TEXT_COLOR
        )
        self.title_label.pack(pady=(35, 10))
        
        # Stats Grid
        self.grid_frame = ctk.CTkFrame(self.center_card, fg_color="transparent")
        self.grid_frame.pack(expand=True, fill="both", padx=40, pady=10)
        
        # Initialize display labels
        self.played_val = self.create_stat_card("GAMES PLAYED", 0, 0, 0, "#3B82F6")
        self.wins_val = self.create_stat_card("WINS (VS AI)", 0, 0, 1, SUCCESS_COLOR)
        self.losses_val = self.create_stat_card("LOSSES (VS AI)", 0, 0, 2, DANGER_COLOR)
        self.draws_val = self.create_stat_card("DRAWS", 0, 1, 0, "#64748B")
        self.winrate_val = self.create_stat_card("WIN RATE", "0.0%", 1, 1, "#A855F7")
        self.streak_val = self.create_stat_card("STREAK (CUR / BEST)", "0 / 0", 1, 2, "#F59E0B")
        
        # Bottom controls
        self.ctrl_frame = ctk.CTkFrame(self.center_card, fg_color="transparent")
        self.ctrl_frame.pack(fill="x", side="bottom", pady=30, padx=40)
        
        self.back_btn = ctk.CTkButton(
            self.ctrl_frame,
            text="Main Menu",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color="#334155",
            hover_color="#475569",
            width=150,
            height=40,
            command=self.go_back
        )
        self.back_btn.pack(side="left")
        
        self.clear_btn = ctk.CTkButton(
            self.ctrl_frame,
            text="Reset Stats",
            font=(FONT_FAMILY, 15, "bold"),
            fg_color=DANGER_COLOR,
            hover_color="#DC2626",
            width=150,
            height=40,
            command=self.reset_stats
        )
        self.clear_btn.pack(side="right")

    def create_stat_card(self, title: str, start_val: Any, row: int, col: int, color_accent: str) -> ctk.CTkLabel:
        """Helper to draw a styled grid box representing a stat."""
        box = ctk.CTkFrame(self.grid_frame, fg_color=BACKGROUND_COLOR, corner_radius=12)
        box.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")
        
        # Allow cells to expand evenly
        self.grid_frame.grid_columnconfigure(col, weight=1)
        self.grid_frame.grid_rowconfigure(row, weight=1)
        
        # Sub-title
        tl = ctk.CTkLabel(box, text=title, font=(FONT_FAMILY, 11, "bold"), text_color=SECONDARY_TEXT_COLOR)
        tl.pack(pady=(15, 2))
        
        # Large value text
        vl = ctk.CTkLabel(box, text=str(start_val), font=(FONT_FAMILY, 24, "bold"), text_color=color_accent)
        vl.pack(pady=(2, 15))
        return vl

    def create_stat_card_double(self, title: str, start_val: Any, row: int, col_start: int, col_span: int, color_accent: str) -> ctk.CTkLabel:
        """Helper to draw a wider grid box (spanning columns) representing a stat."""
        box = ctk.CTkFrame(self.grid_frame, fg_color=BACKGROUND_COLOR, corner_radius=12)
        box.grid(row=row, column=col_start, columnspan=col_span, padx=12, pady=12, sticky="nsew")
        
        tl = ctk.CTkLabel(box, text=title, font=(FONT_FAMILY, 11, "bold"), text_color=SECONDARY_TEXT_COLOR)
        tl.pack(pady=(15, 2))
        
        vl = ctk.CTkLabel(box, text=str(start_val), font=(FONT_FAMILY, 24, "bold"), text_color=color_accent)
        vl.pack(pady=(2, 15))
        return vl

    def on_show(self, **kwargs):
        self.refresh_stats()

    def refresh_stats(self):
        stats = load_stats()
        played = stats.get("games_played", 0)
        wins = stats.get("wins", 0)
        losses = stats.get("losses", 0)
        draws = stats.get("draws", 0)
        curr_streak = stats.get("current_streak", 0)
        best_streak = stats.get("longest_win_streak", 0)
        
        rate = (wins / played * 100) if played > 0 else 0.0
        
        self.played_val.configure(text=str(played))
        self.wins_val.configure(text=str(wins))
        self.losses_val.configure(text=str(losses))
        self.draws_val.configure(text=str(draws))
        self.winrate_val.configure(text=f"{rate:.1f}%")
        self.streak_val.configure(text=f"{curr_streak} / {best_streak}")

    def reset_stats(self):
        stats = {"games_played": 0, "wins": 0, "losses": 0, "draws": 0, "longest_win_streak": 0, "current_streak": 0, "total_moves": 0}
        save_stats(stats)
        play_sound(CLICK_SOUND)
        self.refresh_stats()

    def go_back(self):
        play_sound(CLICK_SOUND)
        self.controller.show_frame("Home")
