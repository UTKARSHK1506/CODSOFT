import tkinter as tk
from tkinter import messagebox
import random

PLAYER = "X"
AI = "O"

def create_buttons():
    for row in range(3):
        for col in range(3):
            button = tk.Button(frame, text="", font=("consolas", 40), width=3, height=1,
                               command=lambda r=row, c=col: next_turn(r, c))
            button.grid(row=row, column=col)
            buttons[row][col] = button

def next_turn(row, col):
    if board[row][col] == "" and label["text"].endswith("turn") and not check_winner(board):
        board[row][col] = player_symbol.get()
        buttons[row][col].config(text=player_symbol.get())
        if check_winner(board):
            messagebox.showinfo("Game Over", f"{player_symbol.get()} wins!")
            label.config(text=f"{player_symbol.get()} wins!")
            return
        elif not empty_spaces(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            label.config(text="It's a tie!")
            return
        player_symbol.set(AI)
        label.config(text=f"{player_symbol.get()} turn")
        root.after(500, ai_move)

def ai_move():
    best_score = -float('inf')
    move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = AI
                score = minimax(board, 0, False)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    move = (r, c)
    if move:
        r, c = move
        board[r][c] = AI
        buttons[r][c].config(text=AI)
        if check_winner(board):
            messagebox.showinfo("Game Over", f"{AI} wins!")
            label.config(text=f"{AI} wins!")
            return
        elif not empty_spaces(board):
            messagebox.showinfo("Game Over", "It's a tie!")
            label.config(text="It's a tie!")
            return
        player_symbol.set(PLAYER)
        label.config(text=f"{player_symbol.get()} turn")

def minimax(state, depth, is_maximizing):
    winner = check_winner(state)
    if winner == AI:
        return 1
    elif winner == PLAYER:
        return -1
    elif not empty_spaces(state):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for r in range(3):
            for c in range(3):
                if state[r][c] == "":
                    state[r][c] = AI
                    score = minimax(state, depth + 1, False)
                    state[r][c] = ""
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for r in range(3):
            for c in range(3):
                if state[r][c] == "":
                    state[r][c] = PLAYER
                    score = minimax(state, depth + 1, True)
                    state[r][c] = ""
                    best_score = min(score, best_score)
        return best_score

def check_winner(state):
    for r in range(3):
        if state[r][0] == state[r][1] == state[r][2] != "":
            return state[r][0]
    for c in range(3):
        if state[0][c] == state[1][c] == state[2][c] != "":
            return state[0][c]
    if state[0][0] == state[1][1] == state[2][2] != "":
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] != "":
        return state[0][2]
    return None

def empty_spaces(state):
    return any(state[r][c] == "" for r in range(3) for c in range(3))

def new_game():
    global board
    board = [["" for _ in range(3)] for _ in range(3)]
    player_symbol.set(random.choice([PLAYER, AI]))
    label.config(text=f"{player_symbol.get()} turn")
    for r in range(3):
        for c in range(3):
            buttons[r][c].config(text="")
    if player_symbol.get() == AI:
        root.after(500, ai_move)

# Setup GUI
root = tk.Tk()
root.title("Tic-Tac-Toe")

player_symbol = tk.StringVar()
player_symbol.set(random.choice([PLAYER, AI]))

label = tk.Label(text=f"{player_symbol.get()} turn", font=('consolas', 40))
label.pack(side="top")

reset_button = tk.Button(text="restart", font=('consolas', 20), command=new_game)
reset_button.pack(side="top")

frame = tk.Frame(root)
frame.pack()

buttons = [[None for _ in range(3)] for _ in range(3)]
board = [["" for _ in range(3)] for _ in range(3)]

create_buttons()
if player_symbol.get() == AI:
    root.after(500, ai_move)

root.mainloop()
