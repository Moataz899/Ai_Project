import random
player = ''
opponent = ''
board = [['_' for _ in range(3)] for _ in range(3)]

def is_moves_left(board):
    return any('_' in row for row in board)

def evaluate(board):
    lines = board + list(zip(*board))
    diagonals = [[board[i][i] for i in range(3)], [board[i][2-i] for i in range(3)]]
    lines += diagonals

    for line in lines:
        if line[0] == line[1] == line[2]:
            if line[0] == player:
                return 10
            elif line[0] == opponent:
                return -10
    return 0

def minimax(board, depth, is_maximizing_player, alpha=-1000, beta=1000):
    score = evaluate(board)

    if score == 10:
        return score
    if score == -10:
        return score
    if not is_moves_left(board):
        return 0

    if is_maximizing_player:
        best = -1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = player
                    best = max(best, minimax(board, depth + 1, False, alpha, beta))
                    board[i][j] = '_'
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        return best
    else:
        best = 1000
        for i in range(3):
            for j in range(3):
                if board[i][j] == '_':
                    board[i][j] = opponent
                    best = min(best, minimax(board, depth + 1, True, alpha, beta))
                    board[i][j] = '_'
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        return best

def find_best_move(board):
    best_val = -1000
    best_move = (-1, -1)

    for i in range(3):
        for j in range(3):
            if board[i][j] == '_':
                board[i][j] = player
                move_val = minimax(board, 0, False)
                board[i][j] = '_'
                if move_val > best_val:
                    best_move = (i, j)
                    best_val = move_val

    return best_move

def render(board):
    print("\n")
    for row in board:
        print(" | ".join(row))
        print("---------")

def human_turn(board):
    while True:
        try:
            move = int(input("Enter your move (1-9): ")) - 1
            row, col = divmod(move, 3)
            if board[row][col] == '_':
                board[row][col] = opponent
                break
            else:
                print("Cell is already taken. Try again.")
        except (ValueError, IndexError):
            print("Invalid input. Please enter a number between 1 and 9.")

def ai_turn(board):
    print("AI is calculating its move...")
    best_move = find_best_move(board)
    board[best_move[0]][best_move[1]] = player

def check_winner(board):
    score = evaluate(board)
    if score == 10:
        return "AI wins!"
    elif score == -10:
        return "Human wins!"
    elif not is_moves_left(board):
        return "It's a draw!"
    return None

def setup_game():
    global player, opponent
    
    while True:
        choice = input("Choose your symbol (X/O): ").lower()
        if choice in ['x', 'o']:
            if choice == 'x':
                player = 'o'
                opponent = 'x'
            else:
                player = 'x'
                opponent = 'o'
            break
        else:
            print("Invalid input. Please choose X or O.")
    
    while True:
        first = input("Do you want to go first? (y/n): ").lower()
        if first in ['y', 'n']:
            return first == 'y'
        else:
            print("Invalid input. Please enter y or n.")

def play_game():
    global board
    print("Welcome to Tic-Tac-Toe!")
    
    while True:
        human_first = setup_game()
        
        board = [['_' for _ in range(3)] for _ in range(3)]
        render(board)

        while True:
            if human_first:
                human_turn(board)
                render(board)
                result = check_winner(board)
                if result:
                    print(result)
                    break

                ai_turn(board)
                render(board)
                result = check_winner(board)
                if result:
                    print(result)
                    break
            else:
                ai_turn(board)
                render(board)
                result = check_winner(board)
                if result:
                    print(result)
                    break

                human_turn(board)
                render(board)
                result = check_winner(board)
                if result:
                    print(result)
                    break

        play_again = input("Do you want to play again? (y/n): ")
        if play_again.lower() != 'y':
            print("Thank you for playing!")
            break


play_game()