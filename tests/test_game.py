import unittest
from src.domain.position import Position
from src.domain.player import Player
from src.domain.board import Board
from src.domain.game import OthelloGame


class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_setup(self):
        mid = self.board.size // 2
        self.assertEqual(
            self.board.cells[mid - 1][mid - 1].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid][mid].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid - 1][mid].occupant, Player.BLACK)
        self.assertEqual(self.board.cells[mid][mid - 1].occupant, Player.BLACK)

    def test_invalid_move_on_occupied_cell(self):
        # 初期配置の場所は既に埋まっているはず
        mid = self.board.size // 2
        pos = Position(mid - 1, mid - 1)
        self.assertFalse(self.board.is_valid_move(pos, Player.BLACK))

    def test_valid_move_and_flip(self):
        # 初期盤面から黒の合法手のひとつ (例: (2,3) が一般的な初手)
        pos = Position(2, 3)
        self.assertTrue(self.board.is_valid_move(pos, Player.BLACK))
        # 手を適用して反転が正しく行われるか確認
        result = self.board.apply_move(pos, Player.BLACK)
        self.assertTrue(result)
        # 適用後は (3,3) のセルが黒に反転しているはず（初期状態では (3,3) は白）
        self.assertEqual(self.board.cells[3][3].occupant, Player.BLACK)


class TestOthelloGame(unittest.TestCase):
    def setUp(self):
        self.game = OthelloGame()

    def test_make_move_changes_turn(self):
        # 初期合法手のひとつ (例: (2,3))
        pos = Position(2, 3)
        current = self.game.current_turn
        result = self.game.make_move(pos)
        self.assertTrue(result)
        self.assertEqual(self.game.current_turn, current.opponent())

    def test_from_state(self):
        # 初期状態のシリアライズされた盤面を用意して再構築する
        board_state = [
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, "W", "B", None, None, None],
            [None, None, None, "B", "W", None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None],
            [None, None, None, None, None, None, None, None]
        ]
        game = OthelloGame.from_state(board_state, "B")
        self.assertEqual(game.current_turn, Player.BLACK)
        self.assertEqual(game.board.cells[3][3].occupant, Player.WHITE)
        self.assertEqual(game.board.cells[3][4].occupant, Player.BLACK)


if __name__ == '__main__':
    unittest.main()
