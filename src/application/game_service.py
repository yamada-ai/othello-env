import pprint
from src.domain.game import OthelloGame
from src.domain.position import Position


def process_move(data: dict) -> dict:
    board_state = data.get("board")
    current_turn = data.get("current_turn")
    row = data.get("row")
    col = data.get("col")
    if board_state is None or current_turn is None or row is None or col is None:
        return {'status': 'error', 'message': '必要なパラメータが不足しています'}

    game = OthelloGame.from_state(board_state, current_turn)
    pos = Position(row, col)
    if game.make_move(pos):
        return {
            'status': 'move accepted',
            'board': serialize_board(game.board),
            'current_turn': game.current_turn.value,
        }
    return {'status': 'invalid move'}


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
    pprint.pprint(_debug_board_str(game.board))
    return {
        'status': 'move accepted' if move_result else 'invalid move',
        'board': serialize_board(game.board),
        'current_turn': game.current_turn.value,
    }


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
