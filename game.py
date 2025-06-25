import tkinter as tk
from tkinter import messagebox
import random

# Game state
player_scores = []
current_player = 0
current_score = 0
total_players = 0
score_labels = []

def start_game():
    global total_players, player_scores, current_player, current_score

    entry = player_entry.get()
    if entry.isdigit():
        players = int(entry)
        if 2 <= players <= 4:
            total_players = players
            player_scores.clear()
            player_scores.extend([0] * total_players)
            current_player = 0
            current_score = 0

            # Update UI
            setup_frame.pack_forget()
            game_frame.pack(pady=10)

            for i in range(4):
                if i < total_players:
                    score_labels[i].config(text=f"Player {i + 1}: 0")
                    score_labels[i].pack()
                else:
                    score_labels[i].pack_forget()

            update_ui()
        else:
            messagebox.showerror("Invalid Input", "Enter players between 2 and 4.")
    else:
        messagebox.showerror("Invalid Input", "Enter a numeric value.")

def roll_dice():
    global current_score
    value = random.randint(1, 6)
    result_label.config(text=f"Player {current_player + 1} rolled: {value}")

    if value == 1:
        messagebox.showinfo("Oops!", "You rolled a 1! Turn ends with 0 points.")
        current_score = 0
        update_turn_score()
        next_player()
    else:
        current_score += value
        update_turn_score()

def hold():
    global current_score, current_player

    # Add current turn score to player’s total
    player_scores[current_player] += current_score
    score_labels[current_player].config(text=f"Player {current_player + 1}: {player_scores[current_player]}")

    if player_scores[current_player] >= 10:
        show_final_scores()
        messagebox.showinfo("Game Over", f"🎉 Player {current_player + 1} wins with {player_scores[current_player]} points!")
        reset_game()
        return

    current_score = 0
    update_turn_score()
    next_player()

def next_player():
    global current_player
    current_player = (current_player + 1) % total_players
    update_ui()

def update_ui():
    current_label.config(text=f"Current Turn: Player {current_player + 1}")
    update_turn_score()
    result_label.config(text="")

def update_turn_score():
    turn_score_label.config(text=f"Turn Score: {current_score}")

def reset_game():
    setup_frame.pack(pady=20)
    game_frame.pack_forget()
    player_entry.delete(0, tk.END)

def show_final_scores():
    score_summary = "\n".join([f"Player {i + 1}: {score} points" for i, score in enumerate(player_scores)])
    messagebox.showinfo("Final Scores", score_summary)

# GUI setup
root = tk.Tk()
root.title("Multiplayer Dice Game")
root.geometry("400x500")

# Setup frame
setup_frame = tk.Frame(root)
tk.Label(setup_frame, text="Enter number of players (2–4):").pack(pady=10)
player_entry = tk.Entry(setup_frame)
player_entry.pack()
tk.Button(setup_frame, text="Start Game", command=start_game).pack(pady=10)
setup_frame.pack(pady=20)

# Game frame
game_frame = tk.Frame(root)

current_label = tk.Label(game_frame, text="", font=("Helvetica", 14))
current_label.pack(pady=5)

scoreboard_frame = tk.Frame(game_frame)
scoreboard_frame.pack()

for i in range(4):  # Max 4 players
    lbl = tk.Label(scoreboard_frame, text=f"Player {i + 1}: 0", font=("Helvetica", 12))
    score_labels.append(lbl)

turn_score_label = tk.Label(game_frame, text="Turn Score: 0", font=("Helvetica", 12))
turn_score_label.pack(pady=5)

result_label = tk.Label(game_frame, text="", font=("Helvetica", 12))
result_label.pack(pady=5)

tk.Button(game_frame, text="Roll Dice", command=roll_dice).pack(pady=5)
tk.Button(game_frame, text="Hold", command=hold).pack(pady=5)
tk.Button(game_frame, text="Reset Game", command=reset_game).pack(pady=10)

root.mainloop()

