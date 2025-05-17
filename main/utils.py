import random

SIZE = 10
SHIP_CONFIG = {
    4: 1,
    3: 2,
    2: 3,
    1: 4
}

def create_board():
    return [['.' for _ in range(SIZE)] for _ in range(SIZE)]

def is_valid_placement(board, x, y, length, horizontal):
    if horizontal:
        if x + length > SIZE:
            return False
        for i in range(length):
            if board[y][x + i] != '.':
                return False
    else:
        if y + length > SIZE:
            return False
        for i in range(length):
            if board[y + i][x] != '.':
                return False
    return True

def place_ship(board, x, y, length, horizontal):
    for i in range(length):
        if horizontal:
            board[y][x + i] = 'S'
        else:
            board[y + i][x] = 'S'

def generate_ships():
    board = create_board()
    for length, count in SHIP_CONFIG.items():
        for _ in range(count):
            while True:
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                horizontal = random.choice([True, False])
                if is_valid_placement(board, x, y, length, horizontal):
                    place_ship(board, x, y, length, horizontal)
                    break
    return board
