import chess.pgn

def get_unique_moves_from_pgn(file_path):
    unique_moves = set()

    with open(file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            for move in game.mainline_moves():
                unique_moves.add(move.uci())

    return len(unique_moves)

def get_max_sequence_length_from_pgn(file_path):
    max_sequence_length = 0

    with open(file_path) as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:
                break

            # Count the number of moves in the current game
            moves_count = sum(1 for _ in game.mainline_moves())

            # Update the maximum sequence length if needed
            max_sequence_length = max(max_sequence_length, moves_count)

    return max_sequence_length
