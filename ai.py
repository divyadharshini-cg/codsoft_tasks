# ai.py
"""Decision making engine for the Tic‑Tac‑Toe AI.
Implements various difficulties ranging from random selections (Easy)
to flawless Alpha-Beta Minimax search (Expert).
"""
import random
from typing import List
from constants import Difficulty
from game import TicTacToeGame

def get_ai_move(game: TicTacToeGame, difficulty: Difficulty, ai_player: str) -> int:
    """Computes and returns the index of the next move for the AI.
    
    Args:
        game: Current TicTacToeGame instance.
        difficulty: The selected Difficulty level.
        ai_player: The AI's symbol ("X" or "O").
        
    Returns:
        The chosen board index (0-8).
    """
    available_moves = game.get_available_moves()
    if not available_moves:
        raise ValueError("No available moves left on the board.")

    # 1. Easy Difficulty: Random moves
    if difficulty == Difficulty.EASY:
        return random.choice(available_moves)

    # 2. Medium Difficulty: 30% chance of random, 70% chance of optimal
    elif difficulty == Difficulty.MEDIUM:
        if random.random() < 0.3:
            return random.choice(available_moves)

    # 3. Hard & Expert Difficulty: Minimax tree search.
    # Expert specifically utilizes alpha-beta pruning, although they result in the same move selection.
    use_pruning = (difficulty in (Difficulty.EXPERT, Difficulty.HARD, Difficulty.MEDIUM))
    
    opponent = "O" if ai_player == "X" else "X"
    best_score = -float('inf')
    best_moves = []

    # Iterate through all available moves and run minimax
    for move in available_moves:
        game.board[move] = ai_player
        score = _minimax(game.board, 0, False, ai_player, opponent, -float('inf'), float('inf'), use_pruning)
        game.board[move] = ""
        
        if score > best_score:
            best_score = score
            best_moves = [move]
        elif score == best_score:
            best_moves.append(move)

    # Return one of the tied best moves to avoid predictable gameplay
    return random.choice(best_moves)

def _check_board_winner(board: List[str]) -> str:
    """Helper to check current winner on a list-based board state."""
    lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for a, b, c in lines:
        if board[a] != "" and board[a] == board[b] == board[c]:
            return board[a]
    if "" not in board:
        return "DRAW"
    return ""

def _minimax(board: List[str], depth: int, is_maximizing: bool, ai_player: str, opponent: str, alpha: float, beta: float, use_pruning: bool) -> int:
    """Performs the minimax recursion to evaluate optimal outcomes."""
    winner = _check_board_winner(board)
    if winner == ai_player:
        return 10 - depth
    elif winner == opponent:
        return depth - 10
    elif winner == "DRAW":
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = ai_player
                score = _minimax(board, depth + 1, False, ai_player, opponent, alpha, beta, use_pruning)
                board[i] = ""
                best_score = max(best_score, score)
                if use_pruning:
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if board[i] == "":
                board[i] = opponent
                score = _minimax(board, depth + 1, True, ai_player, opponent, alpha, beta, use_pruning)
                board[i] = ""
                best_score = min(best_score, score)
                if use_pruning:
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        return best_score
