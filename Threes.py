import random
import math
import os
import numpy as np


# Creates the matrix that will be used as the board, places 8 starter tiles
def initialize_board():
    board = np.zeros((4, 4), dtype=int)
    for i in range(8):
        create_new_tile(board)
    return board


# Outputs the board for viewing per turn
def print_board(board):
    clear()
    horizontal_border = "+" + " --- +" * len(board)

    for row in board:
        print(horizontal_border)
        row_display = "| " + " | ".join(f"{tile if tile != 0 else ' '}".ljust(3) for tile in row) + " |"
        print(row_display)

    print(horizontal_border)
    print()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

# Creates a new random tile from either 1, 2, or 3 with a higher probability of getting a 1 or 2
def create_new_tile(board):
    empty_pos = [
        (r, c)
        for r in range(4)
        for c in range(4)
        if board[r, c] == 0
    ]
    if empty_pos:
        r, c = random.choice(empty_pos)
        board[r, c] = random.choice([1, 2, 3])


# Checks if there are any valid moves left on the board, if there are none the game ends
def can_move(board):
    if np.any(board == 0):
        return True
    for r in range(4):
        for c in range(4):
            if c < 3 and ((2 < board[r, c] == board[r, c + 1] > 2) or {board[r, c], board[r, c + 1]} == {1, 2}):
                return True
            if r < 3 and ((2 < board[r, c] == board[r + 1, c] > 2) or {board[r + 1, c], board[r, c]} == {1, 2}):
                return True

    return False


# Checks if a move for a given row is valid
def valid_move(initial_board, direction):
    final_board = np.array(initial_board)

    final_board = move_tiles(final_board, direction)

    if np.array_equal(final_board, initial_board):
        return False
    else:
        return True


# Merges two tiles together if possible, shifts tiles over one space to the left if possible
def merge_tiles(input_row):
    can_merge = True
    intermediate_row = np.array(input_row)

    for i in range(3):
        if input_row[i] == 0 and input_row[i + 1] != 0:
            can_merge = False

    for i in range(1):
        if input_row[i] != 0 and (
                (input_row[i] == input_row[i + 1]) or ({input_row[i], input_row[i + 1]} == {1, 2})
        ):
            can_merge = True

    for i in range(1, 4):
        if can_merge and (
                (2 < input_row[i] == input_row[i - 1] > 2)
                or ({input_row[i], input_row[i - 1]} == {1, 2})
        ):
            if i == 1 or input_row[i - 1] != 0 and intermediate_row[i - 1] != 0:
                intermediate_row[i] = input_row[i] + input_row[i - 1]
                intermediate_row[i - 1] = 0
                can_merge = False
                break

    output_row = np.array(intermediate_row)

    for i in range(3):
        if output_row[i] == 0 and output_row[i + 1] != 0:
            output_row[i], output_row[i + 1] = intermediate_row[i + 1], 0

    return output_row


# Moves tiles given a w/a/s/d input and merges tiles if possible, returns updated board after the move is done
def move_tiles(board, direction):
    if direction == 'a':
        for i in range(4):
            board[i] = np.array(merge_tiles(board[i]))

    elif direction == 'd':
        board = np.fliplr(board)
        for i in range(4):
            board[i] = np.array(merge_tiles(board[i]))
        board = np.fliplr(board)

    elif direction == 'w':
        board = np.rot90(board, k=1, axes=(0, 1))
        for i in range(4):
            board[i] = np.array(merge_tiles(board[i]))
        board = np.rot90(board, k=-1, axes=(0, 1))

    elif direction == 's':
        board = np.rot90(board, k=-1, axes=(0, 1))
        for i in range(4):
            board[i] = np.array(merge_tiles(board[i]))
        board = np.rot90(board, k=1, axes=(0, 1))

    return board


# Displays the total score at the end of the game, only scores tiles with a value of 3 or greater
def score(board):
    total_score = 0

    for row in board:
        for tile in row:
            if tile >= 3:
                total_score += int(3 ** (math.log((tile / 3), 2) + 1))

    return total_score


# Runs the game by initializing the board, printing each move, checking for move validity, creating new tiles
def game():
    board = initialize_board()
    while can_move(board):
        print_board(board)

        if can_move(board):
            direction = input('Move (w/a/s/d): ').lower()
            if direction in ('w', 'a', 's', 'd'):
                if valid_move(board, direction):
                    board = move_tiles(board, direction)
                    create_new_tile(board)

                    if 768 in board:
                        print_board(board)
                        print('You win! Congratulations!')
                        print('Your score:', score(board))
                        return
                else:
                    print("No moves in that direction, please try another direction.")
            else:
                print('Invalid input, please enter w/a/s/d.')
        elif not can_move(board):
            break

    print_board(board)
    print('Out of moves!')
    print('Your score:', score(board))


game()
