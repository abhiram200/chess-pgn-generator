import chess
import chess.svg
import chess.pgn
import chess.engine
import datetime
import random
import platform
from time import sleep
from IPython.display import SVG
from num_unique_move_in_dataset import get_max_sequence_length_from_pgn, get_unique_moves_from_pgn

board = chess.Board()
board

print("Higher the depth more large sequence length and unique moves.\nBut also increase the time taken to calculate each move")
depth = int(input("Enter a depth value (recommended max value is 2): "))


# Points for pieces for board evaluation

pawntable = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

knightstable = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]
bishopstable = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]
rookstable = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]
queenstable = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]
kingstable = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

# check if the game is still going on

def evaluate_board():
    
    if board.is_checkmate():
            if board.turn:
                return -9999
            else:
                return 9999
    if board.is_stalemate():
            return 0
    if board.is_insufficient_material():
            return 0
        
    # calculate the total number of pieces so that we can pass it into our material function 
    
    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))
    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))
    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))
    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))
    
    # let’s calculate the scores.
    
    material = 100 * (wp - bp) + 320 * (wn - bn) + 330 * (wb - bb) + 500 * (wr - br) + 900 * (wq - bq)
    pawnsq = sum([pawntable[i] for i in board.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pawntable[chess.square_mirror(i)]
                           for i in board.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([knightstable[i] for i in board.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-knightstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bishopstable[i] for i in board.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bishopstable[chess.square_mirror(i)]
                               for i in board.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rookstable[i] for i in board.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rookstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([queenstable[i] for i in board.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-queenstable[chess.square_mirror(i)]
                             for i in board.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kingstable[i] for i in board.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kingstable[chess.square_mirror(i)]
                           for i in board.pieces(chess.KING, chess.BLACK)])
    
    eval = material + pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq
    if board.turn:
        return eval
    else:
        return -eval

def selectmove(move):

    bestMove = chess.Move.null()
    bestValue = -99999
    alpha = -100000
    beta = 100000
    for move in board.legal_moves:
        board.push(move)
        boardValue = -alphabeta(-beta, -alpha, depth - 1)
        if boardValue > bestValue:
            bestValue = boardValue
            bestMove = move
        if (boardValue > alpha):
            alpha = boardValue
        board.pop()
    return bestMove

def alphabeta(alpha, beta, depthleft):
    bestscore = -9999
    if (depthleft == 0):
        return quiesce(alpha, beta)
    for move in board.legal_moves:
        board.push(move)
        score = -alphabeta(-beta, -alpha, depthleft - 1)
        board.pop()
        if (score >= beta):
            return score
        if (score > bestscore):
            bestscore = score
        if (score > alpha):
            alpha = score
    return bestscore

def quiesce(alpha, beta):
    stand_pat = evaluate_board()
    if (stand_pat >= beta):
        return beta
    if (alpha < stand_pat):
        alpha = stand_pat
    for move in board.legal_moves:
            if board.is_capture(move):
                board.push(move)
                score = -quiesce(-beta, -alpha)
                board.pop()
                if (score >= beta):
                        return beta
                if (score > alpha):
                        alpha = score
    return alpha



if platform.system() == 'Windows':
    stockfish_executable = "./stockfish"
else:
    stockfish_executable = "./stockfish_deb"



# ENGINE VS STOCKFISH
engine = chess.engine.SimpleEngine.popen_uci(stockfish_executable)

num_rounds = int(input("Enter the number of rounds: "))
i = 0

while i < num_rounds:
    i += 1
    count = 0
    movehistory = []
    game = chess.pgn.Game()
    board = chess.Board()
    
    # Randomly choose the color for your engine each time
    color = random.choice([chess.WHITE, chess.BLACK])
    your_engine_name = "sno0p3r" if color == chess.WHITE else "Stockfish"
    opponent_name = "Stockfish" if your_engine_name == "sno0p3r" else "sno0p3r"

    while not board.is_game_over(claim_draw=True):
        count += 1
        print(f'\n{count}]\n')
        if board.turn == color:
            move = selectmove(3)  # Your engine's move
            movehistory.append(move)
            board.push(move)
            print(f'{your_engine_name}\'s move:')
        else:
            move = engine.play(board, chess.engine.Limit(time=0.1))  # Stockfish's move
            movehistory.append(move.move)
            board.push(move.move)
            print(f'{opponent_name}\'s move:')
        print(board)

    game.add_line(movehistory)
    game.headers["Event"] = "Engine Tournament 2024"
    game.headers["Site"] = "Dell G15"
    game.headers["Date"] = str(datetime.datetime.now().date())
    game.headers["Round"] = i
    game.headers["White"] = your_engine_name
    game.headers["Black"] = opponent_name
    game.headers["Result"] = str(board.result(claim_draw=True))
    print(game)
    SVG(chess.svg.board(board=board, size=400))

    file_path = 'dataset1.pgn'
    with open(file_path, 'a') as file:
        file.write(str(game))
        file.write("\n\n")
    
    print("Database updated!!!")
    
    
sleep(1)

print("Checking for number of unique moves and max sequence length of the generated dataset...")

seq_length = get_max_sequence_length_from_pgn('dataset1.pgn')
unique_moves = get_unique_moves_from_pgn('dataset1.pgn')

sleep(1)

print("Max Sequence Length: ", seq_length)
print("Unique Moves: ", unique_moves)

