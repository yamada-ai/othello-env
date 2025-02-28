from dataclasses import dataclass, field
from .board import Board
from .position import Position
from .player import Player


@dataclass
class OthelloGame:
    board: Board = field(default_factory=Board)
    current_turn: Player = Player.BLACK

    def make_move(self, pos: Position) -> bool:
        if self.board.apply_move(pos, self.current_turn):
            self.current_turn = self.current_turn.opponent()
            return True
        return False

    @classmethod
    def from_state(cls, board_state: list, current_turn: str) -> 'OthelloGame':
        board = Board(size=len(board_state))
        # 再構築時はセル単位で設定（初期化済みの状態を上書き）
        for i in range(len(board_state)):
            for j in range(len(board_state[i])):
                cell_value = board_state[i][j]
                if cell_value == 'B':
                    board.cells[i][j].occupant = Player.BLACK
                elif cell_value == 'W':
                    board.cells[i][j].occupant = Player.WHITE
                else:
                    board.cells[i][j].occupant = None
        turn = Player.BLACK if current_turn == 'B' else Player.WHITE
        return cls(board=board, current_turn=turn)
