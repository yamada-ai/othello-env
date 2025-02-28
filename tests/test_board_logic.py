import unittest
from src.domain.board import Board
from src.domain.position import Position
from src.domain.player import Player

class TestBoardLogic(unittest.TestCase):
    def setUp(self):
        # 毎回初期状態の Board を生成
        self.board = Board()
    
    def test_initial_setup_validity(self):
        # 初期配置が正しく行われているか
        mid = self.board.size // 2
        self.assertEqual(self.board.cells[mid - 1][mid - 1].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid][mid].occupant, Player.WHITE)
        self.assertEqual(self.board.cells[mid - 1][mid].occupant, Player.BLACK)
        self.assertEqual(self.board.cells[mid][mid - 1].occupant, Player.BLACK)
    
    def test_invalid_move_on_occupied_cell(self):
        # 初期配置済みのセルには手が打てない
        mid = self.board.size // 2
        pos = Position(mid - 1, mid - 1)
        self.assertFalse(self.board.is_valid_move(pos, Player.BLACK))
    
    def test_valid_move_single_direction(self):
        # 一方向の反転が行われるケース
        # 盤面をカスタムセットアップして、たとえば右方向のみで反転が起こるような状態を作成
        # 盤面の中央付近で、左側に相手の石、さらに左に自分の石があるケース
        # ここでは、(3,4) に相手（W）があり、(3,3) に自分（B）がある状態にして、
        # (3,5) に手を打つと、右方向の (3,4) が反転するケースを作る
        # まずは初期状態をクリア
        for row in self.board.cells:
            for cell in row:
                cell.occupant = None
        
        # カスタムセットアップ
        # (3,3) に黒、(3,4) に白
        self.board.cells[3][3].occupant = Player.BLACK
        self.board.cells[3][4].occupant = Player.WHITE
        
        # (3,5) に手を打てるかどうか確認
        pos = Position(3,5)
        self.assertTrue(self.board.is_valid_move(pos, Player.BLACK))
        result = self.board.apply_move(pos, Player.BLACK)
        self.assertTrue(result)
        # (3,4) が黒に反転しているはず
        self.assertEqual(self.board.cells[3][4].occupant, Player.BLACK)
    
    def test_valid_move_multiple_directions(self):
        # 複数方向に反転が起こるケース
        # 盤面の中央付近で、上下左右や斜めすべてで条件を整えるのは複雑だが、
        # ここでは右下方向と下方向の2方向での反転が起こるケースを作成
        for row in self.board.cells:
            for cell in row:
                cell.occupant = None

        # セットアップ: (2,2) に黒、(2,3) と (3,2) に白、(3,3) に黒があるとする
        self.board.cells[2][2].occupant = Player.BLACK
        self.board.cells[2][3].occupant = Player.WHITE
        self.board.cells[3][2].occupant = Player.WHITE
        self.board.cells[3][3].occupant = Player.BLACK

        # (2,4) に手を打つと、右方向の (2,3) が反転するはず
        pos1 = Position(2,4)
        self.assertTrue(self.board.is_valid_move(pos1, Player.BLACK))
        result1 = self.board.apply_move(pos1, Player.BLACK)
        self.assertTrue(result1)
        self.assertEqual(self.board.cells[2][3].occupant, Player.BLACK)

        # (4,2) に手を打つと、下方向の (3,2) が反転するはず
        pos2 = Position(4,2)
        self.assertTrue(self.board.is_valid_move(pos2, Player.BLACK))
        result2 = self.board.apply_move(pos2, Player.BLACK)
        self.assertTrue(result2)
        self.assertEqual(self.board.cells[3][2].occupant, Player.BLACK)
    
    def test_move_out_of_bounds(self):
        # 境界外への手は無効
        pos = Position(-1, 0)
        self.assertFalse(self.board.is_valid_move(pos, Player.BLACK))
        pos2 = Position(8, 8)
        self.assertFalse(self.board.is_valid_move(pos2, Player.BLACK))

if __name__ == '__main__':
    unittest.main()
