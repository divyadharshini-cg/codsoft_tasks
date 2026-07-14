# game.py
"""Core logic and board representation for a standard 3x3 Tic‑Tac‑Toe game.
Tracks turn-taking, move legality, and checks for winners or draw states.
"""
from typing import List
from constants import GameState

class TicTacToeGame:
    def __init__(self):
        self.board: List[str] = [""] * 9
        self.current_player: str = "X"
        self.state: GameState = GameState.IN_PROGRESS
        self.winner_cells: List[int] = []

    def reset(self, starting_player: str = "X"):
        """Resets the game state and board to start a new match."""
        self.board = [""] * 9
        self.current_player = starting_player
        self.state = GameState.IN_PROGRESS
        self.winner_cells = []

    def get_available_moves(self) -> List[int]:
        """Returns the list of indices (0-8) that are currently empty."""
        return [i for i, cell in enumerate(self.board) if cell == ""]

    def make_move(self, index: int) -> bool:
        """Attempts to place the current player's mark at index.
        Returns True if the move was successful, otherwise False.
        """
        if index < 0 or index > 8:
            return False
        if self.state != GameState.IN_PROGRESS or self.board[index] != "":
            return False
        
        self.board[index] = self.current_player
        self._update_state()
        
        if self.state == GameState.IN_PROGRESS:
            self.current_player = "O" if self.current_player == "X" else "X"
        return True

    def _update_state(self) -> None:
        """Scans the board to see if any player has won, or if the board is fully drawn."""
        lines = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
            (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
            (0, 4, 8), (2, 4, 6)              # Diagonals
        ]
        
        for a, b, c in lines:
            if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                self.winner_cells = [a, b, c]
                self.state = GameState.X_WON if self.board[a] == "X" else GameState.O_WON
                return
                
        if "" not in self.board:
            self.state = GameState.DRAW
            return
            
        self.state = GameState.IN_PROGRESS
