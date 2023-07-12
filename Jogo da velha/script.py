from flask import Flask, render_template, request

app = Flask(__name__)

board = [" ", " ", " ", " ", " ", " ", " ", " ", " "]
current_player = "X"

@app.route("/")
def home():
    return render_template("index.html", board=board)

@app.route("/make_move", methods=["POST"])
def make_move():
    position = int(request.form["position"])
    global current_player
    if board[position] == " ":
        board[position] = current_player
        if check_win(current_player):
            game_result = f"O jogador {current_player} venceu!"
        elif " " not in board:
            game_result = "Empate!"
        else:
            current_player = "O" if current_player == "X" else "X"
            game_result = None
    else:
        game_result = "Posição inválida. Tente novamente."
    return render_template("index.html", board=board, game_result=game_result)

def check_win(player):
    winning_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]

    for condition in winning_conditions:
        if (
            board[condition[0]] == player and
            board[condition[1]] == player and
            board[condition[2]] == player
        ):
            return True

    return False

if __name__ == "__main__":
    app.run(debug=True)
