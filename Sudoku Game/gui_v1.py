import tkinter as tk
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")

        # Original Sudoku board (0 represents empty cells)
        self.initial_board = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
        self.board = [row[:] for row in self.initial_board]  # Copy for game state
        self.create_grid()
        self.create_buttons()

    def create_grid(self):
        """ Create the Sudoku grid """
        self.grid = []
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(self.root, width=4, font=('Arial', 18),
                                 justify='center', bd=2, relief='solid')
                entry.grid(row=i, column=j, padx=5, pady=5)
                if self.initial_board[i][j] != 0:  # Pre-filled cells
                    entry.insert(tk.END, str(self.initial_board[i][j]))
                    entry.config(state='disabled', disabledbackground="lightgray")
                else:
                    entry.bind('<KeyRelease>', lambda event, x=i, y=j: self.handle_user_input(event, x, y))
                row.append(entry)
            self.grid.append(row)

    def create_buttons(self):
        """ Create buttons for Solve, AI Move, and Clear """
        solve_btn = tk.Button(self.root, text="Solve", width=10, height=2, command=self.solve)
        solve_btn.grid(row=9, column=0, columnspan=2, pady=10)

        self.ai_btn = tk.Button(self.root, text="AI Move", width=10, height=2, command=self.ai_move)
        self.ai_btn.grid(row=9, column=2, columnspan=2, pady=10)

        clear_btn = tk.Button(self.root, text="Clear", width=10, height=2, command=self.clear_grid)
        clear_btn.grid(row=9, column=4, columnspan=2, pady=10)

    def handle_user_input(self, event, row, col):
        """ Handle user input and validate it in the same cell """
        try:
            value = int(self.grid[row][col].get())

            # Check if value is valid in this cell
            if not (1 <= value <= 9):  # Check if the value is within 1-9
                raise ValueError

            # Temporarily clear the cell to validate the input
            original_value = self.board[row][col]
            self.board[row][col] = 0

            if self.is_safe(row, col, value):
                self.board[row][col] = value  # Place the value if safe
                self.grid[row][col].config(state='disabled', disabledbackground="lightblue")
                print(f"Valid input: {value} at ({row}, {col})")
            else:
                self.grid[row][col].delete(0, tk.END)
                self.board[row][col] = original_value  # Restore original value
                print(f"Invalid input: {value} at ({row}, {col})")

        except ValueError:
            # If input is not an integer or invalid, reset the cell
            self.grid[row][col].delete(0, tk.END)
            print(f"Invalid input at ({row}, {col})")

    def solve(self):
        """ Solve the Sudoku puzzle using backtracking """
        self.board = [row[:] for row in self.initial_board]  # Reset to initial board
        if self.solve_sudoku(0, 0):
            self.update_grid()
            print("Sudoku Solved!")
        else:
            print("No solution exists!")

    def solve_sudoku(self, row, col):
        """ Backtracking solver for Sudoku """
        if col == 9:
            if row == 8:
                return True
            row += 1
            col = 0

        if self.board[row][col] > 0:
            return self.solve_sudoku(row, col + 1)

        for num in range(1, 10):
            if self.is_safe(row, col, num):
                self.board[row][col] = num
                if self.solve_sudoku(row, col + 1):
                    return True
                self.board[row][col] = 0

        return False

    def is_safe(self, row, col, num):
        """ Check if placing a number is safe """
        # Check row
        for i in range(9):
            if i != col and self.board[row][i] == num:
                return False

        # Check column
        for i in range(9):
            if i != row and self.board[i][col] == num:
                return False

        # Check 3x3 box
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if (start_row + i != row or start_col + j != col) and self.board[start_row + i][start_col + j] == num:
                    return False

        return True

    def update_grid(self):
        """ Update the grid with solved board values """
        for i in range(9):
            for j in range(9):
                if self.initial_board[i][j] == 0:  # Update only empty cells
                    self.grid[i][j].delete(0, tk.END)
                    self.grid[i][j].insert(tk.END, str(self.board[i][j]))
                    self.grid[i][j].config(state='disabled', disabledbackground="lightgreen")

    def ai_move(self):
        """ AI makes a random valid move """
        empty_cells = [(i, j) for i in range(9) for j in range(9) if self.board[i][j] == 0]
        if not empty_cells:
            print("No more moves available.")
            return

        while empty_cells:
            i, j = random.choice(empty_cells)
            num = random.randint(1, 9)
            if self.is_safe(i, j, num):
                self.board[i][j] = num
                self.grid[i][j].delete(0, tk.END)
                self.grid[i][j].insert(tk.END, str(num))
                self.grid[i][j].config(state='disabled', disabledbackground="lightyellow")
                print(f"AI placed {num} at ({i}, {j})")
                return
            else:
                empty_cells.remove((i, j))

        print("AI could not make a move!")

    def clear_grid(self):
        """ Clear the grid to reset the game """
        self.board = [row[:] for row in self.initial_board]
        for i in range(9):
            for j in range(9):
                self.grid[i][j].config(state='normal', disabledbackground="white")
                if self.initial_board[i][j] == 0:
                    self.grid[i][j].delete(0, tk.END)
                else:
                    self.grid[i][j].delete(0, tk.END)
                    self.grid[i][j].insert(tk.END, str(self.initial_board[i][j]))
                    self.grid[i][j].config(state='disabled', disabledbackground="lightgray")
        print("Grid cleared!")

# Run the Sudoku GUI
root = tk.Tk()
gui = SudokuGUI(root)
root.mainloop()
