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
        # 初期配置の確認: 中央4セルが決まった色になっているか
        self.assertEqual(
            self.board.cells[mid - 1][mid - 1].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid][mid].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid - 1][mid].occupant, Player.BLACK)
        self.assertEqual(self.board.cells[mid][mid - 1].occupant, Player.BLACK)

    def test_invalid_move_on_occupied_cell(self):
        # 初期配置済みのセルは既に占有済みなので、移動できないはず
        mid = self.board.size // 2
        pos = Position(mid - 1, mid - 1)
        self.assertFalse(self.board.is_valid_move(pos, Player.BLACK))

    def test_valid_move_and_flip(self):
        # 例として、黒の合法手のひとつである (2,3) をテストする
        pos = Position(2, 3)
        self.assertTrue(self.board.is_valid_move(pos, Player.BLACK))
        result = self.board.apply_move(pos, Player.BLACK)
        self.assertTrue(result)
        # 適用後、盤面の特定セルが反転していることを確認
        self.assertEqual(self.board.cells[3][3].occupant, Player.BLACK)

    def test_get_valid_moves(self):
        # 初期状態で、どちらかのプレイヤーに合法手が存在するはず
        valid_moves_black = self.board.get_valid_moves(Player.BLACK)
        valid_moves_white = self.board.get_valid_moves(Player.WHITE)
        self.assertIsInstance(valid_moves_black, list)
        self.assertIsInstance(valid_moves_white, list)
        # 合法手リストに含まれる全ての手が有効か確認
        for move in valid_moves_black:
            self.assertTrue(self.board.is_valid_move(move, Player.BLACK))
        for move in valid_moves_white:
            self.assertTrue(self.board.is_valid_move(move, Player.WHITE))

    def test_has_valid_move(self):
        self.assertTrue(self.board.has_valid_move(Player.BLACK))
        self.assertTrue(self.board.has_valid_move(Player.WHITE))

    def test_is_full(self):
        # すべてのセルに石を置いて盤面を満杯にする
        for row in self.board.cells:
            for cell in row:
                cell.occupant = Player.BLACK
        self.assertTrue(self.board.is_full())

    def test_count_discs(self):
        # 初期盤面では、黒・白それぞれ2個ずつのはず
        black, white = self.board.count_discs()
        self.assertEqual(black, 2)
        self.assertEqual(white, 2)


class TestOthelloGame(unittest.TestCase):
    def setUp(self):
        self.game = OthelloGame()

    def test_make_move_changes_turn(self):
        # 合法手 (2,3) を適用した場合、ターンが交代することを確認
        pos = Position(2, 3)
        current = self.game.current_turn
        result = self.game.make_move(pos)
        self.assertTrue(result)
        self.assertEqual(self.game.current_turn, current.opponent())

    def test_from_state(self):
        # シリアライズされた盤面状態からゲームを再構築するテスト
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

    def test_game_over_and_reward(self):
        # ゲーム終了状態を作るために盤面を満杯にする（黒が大多数の場合）
        for row in self.game.board.cells:
            for cell in row:
                cell.occupant = Player.BLACK
        # 例として、いくつかだけ白にしておく
        self.game.board.cells[0][0].occupant = Player.WHITE
        self.game.board.cells[0][1].occupant = Player.WHITE
        # ゲーム終了判定
        self.assertTrue(self.game.is_game_over())
        winner = self.game.get_winner()
        # 黒の数が多いはずなので、勝者は黒
        self.assertEqual(winner, Player.BLACK)
        # 報酬計算のテスト（黒:+1, 白:-1）
        self.assertEqual(self.game.calculate_reward(Player.BLACK), 1.0)
        self.assertEqual(self.game.calculate_reward(Player.WHITE), -1.0)


if __name__ == '__main__':
    unittest.main()
