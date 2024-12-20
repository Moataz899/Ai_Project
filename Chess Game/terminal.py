import copy

PIECE_VALUES = {
    "K": 10000, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100,
    "k": -10000, "q": -900, "r": -500, "b": -330, "n": -320, "p": -100
}

def create_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"]
    ]


def print_board(board):
    print("\n  a b c d e f g h")
    for i, row in enumerate(board):
        print(8 - i, " ".join(row), 8 - i)
    print("  a b c d e f g h\n")

def evaluate_board(board):
    score = 0
    for row in board:
        for piece in row:
            if piece in PIECE_VALUES:
                score += PIECE_VALUES[piece]
    return score

def generate_moves(board, is_white):
    moves = []
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if (is_white and piece.isupper()) or (not is_white and piece.islower()):
                if piece.lower() == 'p':
                    moves.extend(generate_pawn_moves(board, row, col, piece))
                else:
                    moves.extend(generate_piece_moves(board, row, col, piece))
    return moves

def generate_pawn_moves(board, row, col, piece):
    moves = []
    direction = -1 if piece.isupper() else 1
    start_row = 6 if piece.isupper() else 1  


    if board[row + direction][col] == ".":
        new_board = copy.deepcopy(board)
        new_board[row + direction][col] = piece
        new_board[row][col] = "."
        moves.append(new_board)


        if row == start_row and board[row + 2 * direction][col] == ".":
            new_board = copy.deepcopy(board)
            new_board[row + 2 * direction][col] = piece
            new_board[row][col] = "."
            moves.append(new_board)


    for dc in [-1, 1]:
        if 0 <= col + dc < 8 and board[row + direction][col + dc] != ".":
            if board[row + direction][col + dc].islower() != piece.islower():  # Enemy piece
                new_board = copy.deepcopy(board)
                new_board[row + direction][col + dc] = piece
                new_board[row][col] = "."
                moves.append(new_board)
    return moves

def generate_piece_moves(board, row, col, piece):
    moves = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            if board[new_row][new_col] == "." or board[new_row][new_col].islower() != piece.islower():
                new_board = copy.deepcopy(board)
                new_board[new_row][new_col] = piece
                new_board[row][col] = "."
                moves.append(new_board)
    return moves

def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0:
        return evaluate_board(board), board

    best_move = None

    if is_maximizing:
        max_eval = float("-inf")
        for move in generate_moves(board, True):
            eval, _ = minimax(move, depth - 1, False, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for move in generate_moves(board, False):
            eval, _ = minimax(move, depth - 1, True, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def player_move(board):
    while True:
        try:
            print("Enter your move (e.g., 'e2 e4'):")
            move = input("Move: ").strip().lower()
            if len(move) != 5 or move[2] != " ":
                raise ValueError("Invalid format. Use 'e2 e4'.")
            
            start, end = move.split()
            start_col, start_row = ord(start[0]) - ord('a'), 8 - int(start[1])
            end_col, end_row = ord(end[0]) - ord('a'), 8 - int(end[1])

            piece = board[start_row][start_col]
            if piece == "." or piece.islower():  
                print("Invalid move. Choose a valid white piece.")
                continue

            new_board = copy.deepcopy(board)
            new_board[end_row][end_col] = piece
            new_board[start_row][start_col] = "."
            return new_board
        except Exception as e:
            print(e)

def main():
    board = create_board()
    print("Initial Board:")
    print_board(board)

    while True:

        print("Your Turn:")
        board = player_move(board)
        print_board(board)

        print("AI's Turn:")
        board = minimax(board, 3, False, float("-inf"), float("inf"))
        print_board(board)

main()
