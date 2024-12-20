import tkinter as tk
from tkinter import messagebox
import random

class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku")
        self.root.configure(bg='black')

        # Configure style
        self.font = ('Arial', 24)
        self.cell_size = 60
        self.selected_cell = None
        self.dragged_number = None

        # Initial Sudoku board
        self.board = [
            [3, 0, 2, 1, 5, 0, 9, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 8, 0],
            [4, 6, 0, 8, 9, 0, 0, 5, 0],
            [5, 0, 1, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 7, 8, 1],
            [0, 0, 0, 0, 3, 5, 0, 0, 0],
            [1, 0, 6, 4, 0, 7, 5, 3, 0],
            [0, 4, 9, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 8, 6, 0, 0, 0, 0]
        ]
        self.initial_board = [row[:] for row in self.board]

        # Create main frame
        self.main_frame = tk.Frame(root, bg='black')
        self.main_frame.pack(padx=20, pady=20)

        self.create_grid()
        self.create_numpad()
        self.create_control_buttons()

        # Bind keyboard and mouse events
        root.bind('<space>', self.new_game)
        self.root.bind('<B1-Motion>', self. drag)
        self.root.bind('<ButtonRelease-1>', self.handle_drop)

    def create_grid(self):
        """Create the Sudoku grid."""
        self.cells = []
        self.grid_frame = tk.Frame(self.main_frame, bg='black', bd=2, relief='solid')
        self.grid_frame.pack(side='left', padx=(0, 20))

        for i in range(9):
            row = []
            for j in range(9):
                cell_frame = self.create_cell_frame(i, j)
                label = self.create_cell_label(cell_frame)
                cell_frame.grid_info = {'row': i, 'column': j}
                cell_frame.bind('<Button-1>', lambda e, row=i, col=j: self.cell_clicked(row, col))
                label.bind('<Button-1>', lambda e, row=i, col=j: self.cell_clicked(row, col))
                row.append(label)
            self.cells.append(row)

        self.update_display()

    def create_cell_frame(self, i, j):
        """Create a frame for a single cell."""
        cell_frame = tk.Frame(
            self.grid_frame,
            width=self.cell_size,
            height=self.cell_size,
            bg='black',
            highlightthickness=1,
            highlightbackground='#333'
        )
        cell_frame.grid_propagate(False)
        cell_frame.grid(row=i, column=j)

        if i % 3 == 0 and i != 0:
            cell_frame.grid(pady=(2, 0))
        if j % 3 == 0 and j != 0:
            cell_frame.grid(padx=(2, 0))

        return cell_frame

    def create_cell_label(self, cell_frame):
        """Create a label for a cell."""
        label = tk.Label(
            cell_frame,
            text='',
            font=self.font,
            bg='black',
            fg='#00ffff',
            justify='center'
        )
        label.place(relx=0.5, rely=0.5, anchor='center')
        return label

    def create_control_buttons(self):
        """Create control buttons (Solve, AI Move, Clear, Reset)."""
        button_frame = tk.Frame(self.root, bg='black')
        button_frame.pack(pady=10)

        # Solve button
        self.create_button(button_frame, "Solve", self.solve_puzzle)

        # AI Move button
        self.create_button(button_frame, "AI Move", self.make_ai_move)

        # Clear button
        self.create_button(button_frame, "Clear", self.clear_board)

        # Reset button
        self.create_button(button_frame, "Reset", self.reset_last_value)

    def create_button(self, parent, text, command):
        """Helper method to create a button."""
        btn = tk.Button(
            parent,
            text=text,
            font=('Arial', 12),
            bg='black',
            fg='#00ffff',
            command=command,
            width=10
        )
        btn.pack(side='left', padx=5)

    def reset_last_value(self):
        """Remove the last value input without clearing all."""
        if self.selected_cell:
            row, col = self.selected_cell
            if self.initial_board[row][col] == 0 and self.board[row][col] != 0:
                self.board[row][col] = 0
                self.cells[row][col].configure(text='')

    def reset_game(self):
        """Reset the game to the initial state."""
        self.board = [row[:] for row in self.initial_board]
        self.selected_cell = None
        self.update_display()
        self.clear_victory_message()

    def clear_victory_message(self):
        """Clear the victory message if it exists."""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Label) and widget.cget('text').startswith('You Won!'):
                widget.destroy()

    def solve_puzzle(self):
        """Solve the entire Sudoku puzzle."""
        if self.solve_sudoku():
            self.update_display()
            if self.check_victory():
                self.show_victory()
        else:
            messagebox.showinfo("Error", "No solution exists for this puzzle!")

    def solve_sudoku(self, row=0, col=0):
        """Recursive function to solve Sudoku."""
        if row == 9:
            return True

        if col == 9:
            return self.solve_sudoku(row + 1, 0)

        if self.board[row][col] != 0:
            return self.solve_sudoku(row, col + 1)

        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.board[row][col] = num
                if self.solve_sudoku(row, col + 1):
                    return True
                self.board[row][col] = 0

        return False

    def make_ai_move(self):
        """Make a single smart move."""
        if not self.selected_cell:
            messagebox.showinfo("Info", "Please select a cell first!")
            return

        row, col = self.selected_cell
        if self.initial_board[row][col] != 0:
            messagebox.showinfo("Info", "This cell is part of the initial puzzle!")
            return

        valid_numbers = [num for num in range(1, 10) if self.is_valid_move(row, col, num)]

        if valid_numbers:
            number = random.choice(valid_numbers)
            self.board[row][col] = number
            self.cells[row][col].configure(text=str(number))

            if self.check_victory():
                self.show_victory()
        else:
            messagebox.showinfo("Info", "No valid moves available for this cell!")

    def clear_board(self):
        """Clear all non-initial cells."""
        for i in range(9):
            for j in range(9):
                if self.initial_board[i][j] == 0:
                    self.board[i][j] = 0
                    self.cells[i][j].configure(text='')

        self.selected_cell = None

    def create_numpad(self):
        """Create the number pad on the right."""
        numpad_frame = tk.Frame(self.main_frame, bg='black')
        numpad_frame.pack(side='right')

        self.number_buttons = []
        for i in range(9):
            btn = tk.Label(
                numpad_frame,
                text=str(i + 1),
                font=self.font,
                width=2,
                height=1,
                relief='solid',
                bd=1,
                bg='black',
                fg='white'
            )
            btn.pack(pady=2)
            btn.bind('<Button-1>', lambda e, num=i+1: self.start_drag(e, num))
            self.number_buttons.append(btn)

    def start_drag(self, event, number):
        """Start dragging a number."""
        self.dragged_number = number

        if hasattr(self, 'drag_label'):
            self.drag_label.destroy()

        self.drag_label = tk.Label(
            self.root,
            text=str(number),
            font=self.font,
            fg='#00ffff',
            bg='black'
        )
        self.drag_label.lift()
        self.drag_label.place(x=event.x_root, y=event.y_root, anchor="center")

    def drag(self, event):
        """Update position of dragged number."""
        if hasattr(self, 'drag_label') and self.dragged_number:
            self.drag_label.place(x=event.x_root, y=event.y_root, anchor="center")

            for i in range(9):
                for j in range(9):
                    cell = self.cells[i][j].master
                    cell_x = cell.winfo_rootx()
                    cell_y = cell.winfo_rooty()
                    if (cell_x <= event.x_root <= cell_x + self.cell_size and 
                        cell_y <= event.y_root <= cell_y + self.cell_size):
                        self.cell_clicked(i, j)
                        return

    def handle_drop(self, event):
        """Handle dropping a number into a cell."""
        if self.dragged_number and self.selected_cell:
            row, col = self.selected_cell
            if self.initial_board[row][col] == 0:
                cell = self.cells[row][col].master
                cell_x = cell.winfo_rootx()
                cell_y = cell.winfo_rooty()
                if (cell_x <= event.x_root <= cell_x + self.cell_size and 
                    cell_y <= event.y_root <= cell_y + self.cell_size):
                    if self.is_valid_move(row, col, self.dragged_number):
                        self.board[row][col] = self.dragged_number
                        self.cells[row][col].configure(text=str(self.dragged_number))
                        if self.check_victory():
                            self.show_victory()

        if hasattr(self, 'drag_label'):
            self.drag_label.destroy()
            delattr(self, 'drag_label')
        self.dragged_number = None

    def cell_clicked(self, row, col):
        """Handle cell selection."""
        if self.initial_board[row][col] == 0:
            if self.selected_cell:
                prev_row, prev_col = self.selected_cell
                self.cells[prev_row][prev_col].master.configure(bg='black')

            self.selected_cell = (row, col)
            self.cells[row][col].master.configure(bg='#333')

    def is_valid_move(self, row, col, num):
        """Check if a move is valid."""
        if any(self.board[row][j] == num for j in range(9) if j != col):
            return False
        if any(self.board[i][col] == num for i in range(9) if i != row):
            return False
        box_row, box_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(box_row, box_row + 3):
            for j in range(box_col, box_col + 3):
                if self.board[i][j] == num and (i != row or j != col):
                    return False
        return True

    def update_display(self):
        """Update the display with current board state."""
        for i in range(9):
            for j in range(9):
                value = self.board[i][j]
                if value != 0:
                    self.cells[i][j].configure(text=str(value))
                else:
                    self.cells[i][j].configure(text='')

    def check_victory(self):
        """Check if the puzzle is solved."""
        return all(self.board[i][j] != 0 for i in range(9) for j in range(9))

    def show_victory(self):
        """Show victory message."""
        victory_label = tk.Label(
            self.root,
            text="You Won!\n\nPress Space to restart!",
            font=('Arial', 16),
            bg='black',
            fg='#00ff00',
            justify='center'
        )
        victory_label.pack()

    def new_game(self, event=None):
        """Start a new game."""
        self.reset_game()
        self.clear_victory_message()


root = tk.Tk()
root.configure(bg='black')
game = SudokuGUI(root)
root.mainloop()