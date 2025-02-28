from dataclasses import dataclass, field
from typing import Optional
from .board import Board
from .player import Player
from .position import Position


@dataclass
class OthelloGame:
    board: Board = field(default_factory=Board)
    current_turn: Player = Player.BLACK

    def make_move(self, pos: Position) -> bool:
        if self.board.apply_move(pos, self.current_turn):
            self.current_turn = self.current_turn.opponent()
            return True
        return False

    def is_game_over(self) -> bool:
        """
        ゲーム終了条件:
         - 両プレイヤーともに合法手がない場合
         - または盤面が満杯の場合
        """
        if self.board.is_full():
            return True
        if not self.board.has_valid_move(Player.BLACK) and not self.board.has_valid_move(Player.WHITE):
            return True
        return False

    def get_winner(self) -> Optional[Player]:
        """
        ゲーム終了時の勝者を返す。
        黒の石数が多ければ Player.BLACK、白が多ければ Player.WHITE、
        同数の場合は None（引き分け）を返す。
        """
        black, white = self.board.count_discs()
        if black > white:
            return Player.BLACK
        elif white > black:
            return Player.WHITE
        else:
            return None

    def is_draw(self) -> bool:
        """
        ゲーム終了かつ勝者が存在しなければ引き分けと判定
        """
        return self.is_game_over() and (self.get_winner() is None)

    def calculate_reward(self, player: Player) -> float:
        """
        勝者に基づく報酬計算:
         - 勝ちの場合: +1
         - 負けの場合: -1
         - 引き分けの場合: 0
        """
        winner = self.get_winner()
        if winner is None:
            return 0.0
        elif winner == player:
            return 1.0
        else:
            return -1.0

    @classmethod
    def from_state(cls, board_state: list, current_turn: str) -> 'OthelloGame':
        board = Board(size=len(board_state))
        # 各セルに対して、文字列での状態（"B", "W", None）を適用
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
