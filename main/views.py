import random
from django.shortcuts import render, redirect
from django.http import JsonResponse
import json

SIZE = 10
MAX_SHIPS = 10


def create_board():
    return [['.' for _ in range(SIZE)] for _ in range(SIZE)]


def start(request):
    return render(request, 'place_ships.html', {'range': range(SIZE)})


def save_ships(request):
    if request.method == 'POST':
        board = json.loads(request.POST.get('board'))
        count = sum(row.count('S') for row in board)
        if count != MAX_SHIPS:
            return render(request, 'place_ships.html', {
                'range': range(SIZE),
                'error': f'Потрібно розставити рівно {MAX_SHIPS} кораблів!'
            })
        request.session['player_board'] = board
        # Генеруємо поле бота з 10 випадковими кораблями
        bot_board = create_board()
        placed = 0
        while placed < MAX_SHIPS:
            x = random.randint(0, SIZE - 1)
            y = random.randint(0, SIZE - 1)
            if bot_board[y][x] == '.':
                bot_board[y][x] = 'S'
                placed += 1
        request.session['bot_board'] = bot_board
        request.session['player_shots'] = []
        request.session['bot_shots'] = []
        return redirect('play')
    return redirect('start')


def play(request):
    player_board_raw = request.session.get('player_board', create_board())
    bot_board_raw = request.session.get('bot_board', create_board())

    player_board = list(enumerate(player_board_raw))
    player_board = [(y, list(enumerate(row))) for y, row in player_board]

    bot_board = list(enumerate(bot_board_raw))
    bot_board = [(y, list(enumerate(row))) for y, row in bot_board]

    return render(request, 'play.html', {
        'player_board': player_board,
        'bot_board': bot_board,
    })


def shot(request):
    x = int(request.GET.get('x'))
    y = int(request.GET.get('y'))
    bot_board = request.session.get('bot_board')
    player_shots = request.session.get('player_shots', [])

    if (x, y) in player_shots:
        return JsonResponse({'hit': None})

    player_shots.append((x, y))
    hit = False

    if bot_board[y][x] == 'S':
        bot_board[y][x] = 'X'
        hit = True
    else:
        bot_board[y][x] = 'O'

    request.session['bot_board'] = bot_board
    request.session['player_shots'] = player_shots

    game_over = all(cell != 'S' for row in bot_board for cell in row)
    result = "🎉 Ти переміг!" if game_over else ""

    return JsonResponse({'hit': hit, 'game_over': game_over, 'result': result})

def bot_shot(request):
    player_board = request.session.get('player_board')
    bot_shots = request.session.get('bot_shots', [])

    while True:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if (x, y) not in bot_shots:
            bot_shots.append((x, y))
            break

    hit = False
    if player_board[y][x] == 'S':
        player_board[y][x] = 'X'
        hit = True
    else:
        player_board[y][x] = 'O'

    request.session['player_board'] = player_board
    request.session['bot_shots'] = bot_shots

    game_over = all(cell != 'S' for row in player_board for cell in row)
    result = "Бот переміг!" if game_over else ""

    return JsonResponse({'x': x, 'y': y, 'hit': hit, 'game_over': game_over, 'result': result})
