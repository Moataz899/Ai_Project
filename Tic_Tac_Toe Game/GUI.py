import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self, master):
        self.master = master
        self.master.title("Tic Tac Toe")
        self.player = ''
        self.opponent = ''
        self.board = [['_' for _ in range(3)] for _ in range(3)]
        self.human_first = True
        self.show_symbol_selection()

    def show_symbol_selection(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        tk.Label(self.master, text="Choose Your Symbol", font=('Arial', 16)).pack(pady=20)
        frame = tk.Frame(self.master)
        frame.pack(pady=20)
        
        tk.Button(frame, text="X", command=lambda: self.set_symbol('x'), 
                  font=('Arial', 14), width=5).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="O", command=lambda: self.set_symbol('o'), 
                  font=('Arial', 14), width=5).pack(side=tk.LEFT, padx=10)

    def set_symbol(self, symbol):
        if symbol == 'x':
            self.player = 'o'
            self.opponent = 'x'
        else:
            self.player = 'x'
            self.opponent = 'o'
            
            self.show_first_turn_selection()

    def show_first_turn_selection(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        tk.Label(self.master, text="Do You Want to Go First?", font=('Arial', 16)).pack(pady=20)
        
        frame = tk.Frame(self.master)
        frame.pack(pady=20)
        
        tk.Button(frame, text="Yes", command=lambda: self.start_game(True), 
                  font=('Arial', 14), width=5).pack(side=tk.LEFT, padx=10)
        tk.Button(frame, text="No", command=lambda: self.start_game(False), 
                  font=('Arial', 14), width=5).pack(side=tk.LEFT, padx=10)

    def start_game(self, human_first):
        self.human_first = human_first
        self.board = [['_' for _ in range(3)] for _ in range(3)]
        
        self.create_board_gui()
        
        if not human_first:
            self.ai_turn()

    def create_board_gui(self):
        for widget in self.master.winfo_children():
            widget.destroy()
        
        self.buttons = []
        for i in range(3):
            row = []
            for j in range(3):
                btn = tk.Button(self.master, text='', font=('Arial', 20), 
                                width=5, height=2,
                                command=lambda r=i, c=j: self.human_turn(r, c))
                btn.grid(row=i, column=j, padx=5, pady=5)
                row.append(btn)
            self.buttons.append(row)

    def human_turn(self, row, col):
        if self.board[row][col] == '_':
            self.board[row][col] = self.opponent
            self.buttons[row][col].config(text=self.opponent.upper())
            
            result = self.check_winner()
            if result:
                self.show_result(result)
                return
            self.ai_turn()

    def ai_turn(self):
        best_move = self.find_best_move()
        
        self.board[best_move[0]][best_move[1]] = self.player
        self.buttons[best_move[0]][best_move[1]].config(text=self.player.upper())
        
        result = self.check_winner()
        if result:
            self.show_result(result)

    def show_result(self, result):
        messagebox.showinfo("Game Over", result)
        if messagebox.askyesno("Play Again", "Do you want to play again?"):
            self.show_symbol_selection()
        else:
            self.master.quit()

    def is_moves_left(self):
        return any('_' in row for row in self.board)

    def evaluate(self):
        lines = self.board + list(zip(*self.board))
        diagonals = [[self.board[i][i] for i in range(3)], 
                     [self.board[i][2-i] for i in range(3)]]
        lines += diagonals

        for line in lines:
            if line[0] == line[1] == line[2]:
                if line[0] == self.player:
                    return 10
                elif line[0] == self.opponent:
                    return -10
        return 0

    def minimax(self, depth, is_maximizing_player, alpha=-1000, beta=1000):
        score = self.evaluate()

        if score == 10: 
            return score
        if score == -10:  
            return score
        if not self.is_moves_left():
            return 0

        if is_maximizing_player:
            best = -1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '_':
                        self.board[i][j] = self.player
                        best = max(best, self.minimax(depth + 1, False, alpha, beta))
                        self.board[i][j] = '_'
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = 1000
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == '_':
                        self.board[i][j] = self.opponent
                        best = min(best, self.minimax(depth + 1, True, alpha, beta))
                        self.board[i][j] = '_'
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def find_best_move(self):
        best_val = -1000
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == '_':
                    self.board[i][j] = self.player
                    move_val = self.minimax(0, False)
                    self.board[i][j] = '_'
                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        return best_move

    def check_winner(self):
        score = self.evaluate()
        if score == 10:
            return "AI wins!"
        elif score == -10:
            return "Human wins!"
        elif not self.is_moves_left():
            return "It's a draw!"
        return None

def main():
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()


main()