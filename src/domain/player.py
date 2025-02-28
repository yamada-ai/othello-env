from enum import Enum


class Player(Enum):
    BLACK = 'B'
    WHITE = 'W'

    def opponent(self) -> 'Player':
        return Player.WHITE if self == Player.BLACK else Player.BLACK
