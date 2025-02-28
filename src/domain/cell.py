from dataclasses import dataclass
from typing import Optional
from .position import Position
from .player import Player


@dataclass
class Cell:
    position: Position
    occupant: Optional[Player] = None

    def is_empty(self) -> bool:
        return self.occupant is None
