import pprint
from src.domain.game import OthelloGame
from src.domain.position import Position
from src.domain.player import Player


def process_move(data: dict) -> dict:
    board_state = data.get("board")
    current_turn = data.get("current_turn")
    row = data.get("row")
    col = data.get("col")
    if board_state is None or current_turn is None or row is None or col is None:
        return {'status': 'error', 'message': '必要なパラメータが不足しています'}

    game = OthelloGame.from_state(board_state, current_turn)
    pos = Position(row, col)
    move_result = game.make_move(pos)
    response = {
        'status': 'move accepted' if move_result else 'invalid move',
        'board': serialize_board(game.board),
        'current_turn': game.current_turn.value,
    }
    # ゲーム終了の場合は、勝者と報酬情報を付与する
    if game.is_game_over():
        winner = game.get_winner()
        response['game_over'] = True
        response['winner'] = winner.value if winner else 'draw'
        # 各プレイヤーの報酬（シンプルに、勝ち:+1, 負け:-1, 引き分け:0）
        response['reward_BLACK'] = game.calculate_reward(Player.BLACK)
        response['reward_WHITE'] = game.calculate_reward(Player.WHITE)
    else:
        response['game_over'] = False

    return response


def process_move_debug(data: dict) -> dict:
    """/move/debug 用の処理。move の結果と、テキストでの盤面可視化も返す"""
    board_state = data.get("board")
    current_turn = data.get("current_turn")
    row = data.get("row")
    col = data.get("col")
    if board_state is None or current_turn is None or row is None or col is None:
        return {'status': 'error', 'message': '必要なパラメータが不足しています'}

    game = OthelloGame.from_state(board_state, current_turn)
    pos = Position(row, col)
    move_result = game.make_move(pos)
    board_str = _debug_board_str(game.board)
    pprint.pprint(board_str)
    response = {
        'status': 'move accepted' if move_result else 'invalid move',
        'board': serialize_board(game.board),
        'current_turn': game.current_turn.value,
        'debug_board': board_str,
    }
    if game.is_game_over():
        winner = game.get_winner()
        response['game_over'] = True
        response['winner'] = winner.value if winner else 'draw'
        response['reward_BLACK'] = game.calculate_reward(Player.BLACK)
        response['reward_WHITE'] = game.calculate_reward(Player.WHITE)
    else:
        response['game_over'] = False
    return response


def get_initial_state() -> dict:
    game = OthelloGame()
    return {
        'board': serialize_board(game.board),
        'current_turn': game.current_turn.value,
    }


def serialize_board(board) -> list:
    serialized = []
    for row in board.cells:
        serialized_row = []
        for cell in row:
            serialized_row.append(
                cell.occupant.value if cell.occupant else None)
        serialized.append(serialized_row)
    return serialized


def _debug_board_str(board) -> str:
    """
    Board の状態を文字列として可視化する。
    各セルは、空なら「.」、黒なら「B」、白なら「W」で表現する。
    """
    lines = []
    for row in board.cells:
        line = ' '.join(
            cell.occupant.value if cell.occupant else '.' for cell in row)
        lines.append(line)
    return "\n".join(lines)
