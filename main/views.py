import random
from django.shortcuts import render, redirect
from django.http import JsonResponse

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


def index(request):
    return render(request, 'game/index.html')


def start_game(request):
    request.session['player_board'] = generate_ships()
    request.session['bot_board'] = generate_ships()
    request.session['player_shots'] = []
    request.session['bot_shots'] = []
    return redirect('play')


def play(request):
    return render(request, 'game/play.html', {
        'player_board': request.session.get('player_board'),
        'bot_board': [["X" if (x, y) in request.session.get('player_shots', []) else '.' for x in range(SIZE)] for y in range(SIZE)]
    })


def player_shot(request):
    x = int(request.GET.get('x'))
    y = int(request.GET.get('y'))
    bot_board = request.session.get('bot_board')
    shots = request.session.get('player_shots', [])
    if (x, y) not in shots:
        shots.append((x, y))
        if bot_board[y][x] == 'S':
            bot_board[y][x] = 'X'
            hit = True
        else:
            bot_board[y][x] = 'O'
            hit = False
        request.session['player_shots'] = shots
        request.session['bot_board'] = bot_board
    else:
        hit = None
    return JsonResponse({'hit': hit})
