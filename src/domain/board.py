from dataclasses import dataclass, field
from typing import List, Tuple, Optional
from .cell import Cell
from .position import Position
from .player import Player


@dataclass
class Board:
    size: int = 8
    cells: List[List[Cell]] = field(init=False)

    def __post_init__(self):
        # 各座標に Cell を生成し初期状態にセット
        self.cells = [
            [Cell(Position(row, col)) for col in range(self.size)]
            for row in range(self.size)
        ]
        self.initialize()

    def initialize(self) -> None:
        mid = self.size // 2
        self.cells[mid - 1][mid - 1].occupant = Player.WHITE
        self.cells[mid][mid].occupant = Player.WHITE
        self.cells[mid - 1][mid].occupant = Player.BLACK
        self.cells[mid][mid - 1].occupant = Player.BLACK

    def get_cell(self, pos: Position) -> Optional[Cell]:
        if 0 <= pos.row < self.size and 0 <= pos.col < self.size:
            return self.cells[pos.row][pos.col]
        return None

    def is_valid_move(self, pos: Position, current_turn: Player) -> bool:
        cell = self.get_cell(pos)
        if cell is None or not cell.is_empty():
            return False

        for direction in self._directions():
            if self._flippable_in_direction(pos, current_turn, direction):
                return True
        return False

    def apply_move(self, pos: Position, current_turn: Player) -> bool:
        if not self.is_valid_move(pos, current_turn):
            return False

        # 自身に石を置く
        self.get_cell(pos).occupant = current_turn
        # 各方向の反転対象を収集して反転
        for direction in self._directions():
            flippable = self._flippable_in_direction(
                pos, current_turn, direction)
            if isinstance(flippable, list) and flippable:
                for cell in flippable:
                    cell.occupant = current_turn
        return True

    def _directions(self) -> List[Tuple[int, int]]:
        return [(-1, 0), (1, 0), (0, -1), (0, 1),
                (-1, -1), (-1, 1), (1, -1), (1, 1)]

    def _flippable_in_direction(self, pos: Position, current_turn: Player, direction: Tuple[int, int]) -> Optional[List[Cell]]:
        """
        指定方向において、反転可能な相手のセルのリストを返す。
        反転対象が存在しない場合は None を返す。
        """
        dr, dc = direction
        r, c = pos.row + dr, pos.col + dc
        flippable = []
        opponent = current_turn.opponent()

        while 0 <= r < self.size and 0 <= c < self.size:
            cell = self.cells[r][c]
            if cell.occupant == opponent:
                flippable.append(cell)
            elif cell.occupant == current_turn:
                return flippable if flippable else None
            else:
                break
            r += dr
            c += dc
        return None
