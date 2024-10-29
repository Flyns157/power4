from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit

# Initialiser le plateau (6 lignes x 7 colonnes)
ROWS = 6
COLUMNS = 7
EMPTY = 0
board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
current_player = 1  # Joueur 1 commence


def check_winner(board, player):
    # Vérifie les lignes
    for row in range(ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row][col + i] == player for i in range(4)):
                return True

    # Vérifie les colonnes
    for col in range(COLUMNS):
        for row in range(ROWS - 3):
            if all(board[row + i][col] == player for i in range(4)):
                return True

    # Vérifie les diagonales montantes
    for row in range(ROWS - 3):
        for col in range(COLUMNS - 3):
            if all(board[row + i][col + i] == player for i in range(4)):
                return True

    # Vérifie les diagonales descendantes
    for row in range(3, ROWS):
        for col in range(COLUMNS - 3):
            if all(board[row - i][col + i] == player for i in range(4)):
                return True

    return False


def reset_board():
    global board, current_player
    board = [[EMPTY for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_player = 1


def init_app(app: Flask)-> SocketIO:
    socketio = SocketIO(app)
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_state', methods=['GET'])
    def get_state():
        return jsonify({"board": board, "current_player": current_player})

    @app.route('/move', methods=['POST'])
    def move():
        global current_player
        col = request.json.get('column')
        if col < 0 or col >= COLUMNS:
            return jsonify({"error": "Invalid column"}), 400

        # Trouver la première ligne vide dans la colonne
        for row in range(ROWS - 1, -1, -1):
            if board[row][col] == EMPTY:
                board[row][col] = current_player
                if check_winner(board, current_player):
                    winner = current_player
                    reset_board()
                    socketio.emit('game_update', {"board": board, "current_player": current_player, "winner": winner})
                    return jsonify({"winner": winner})
                current_player = 3 - current_player
                socketio.emit('game_update', {"board": board, "current_player": current_player})
                return jsonify({"board": board, "current_player": current_player})

        return jsonify({"error": "Column is full"}), 400
    
    return socketio
