import unittest
from webtest import TestApp
from src.infrastructure.server import app as bottle_app


class TestAPIServer(unittest.TestCase):
    def setUp(self):
        self.app = TestApp(bottle_app)

    def test_init_endpoint(self):
        resp = self.app.get('/init')
        self.assertEqual(resp.status_int, 200)
        data = resp.json
        self.assertIn('board', data)
        self.assertIn('current_turn', data)
        # 盤面は 8x8 になっているか確認
        self.assertEqual(len(data['board']), 8)
        self.assertEqual(len(data['board'][0]), 8)

    def test_move_debug_endpoint_valid_move(self):
        # 初期状態を取得
        init_resp = self.app.get('/init')
        init_data = init_resp.json

        # 初期合法手 (例: (2,3) は一般的な初手)
        move_data = init_data.copy()
        move_data['row'] = 2
        move_data['col'] = 3

        resp = self.app.post_json('/move/debug', move_data)
        self.assertEqual(resp.status_int, 200)
        data = resp.json
        self.assertIn('board', data)
        self.assertIn('current_turn', data)

    def test_move_endpoint_invalid_move(self):
        # 初期状態で、既に石が置かれている場所 (例: (3,3) は初期配置で埋まっている)
        init_resp = self.app.get('/init')
        init_data = init_resp.json

        move_data = init_data.copy()
        move_data['row'] = 3
        move_data['col'] = 3

        resp = self.app.post_json('/move', move_data)
        self.assertEqual(resp.status_int, 200)
        data = resp.json
        self.assertEqual(data['status'], 'invalid move')


if __name__ == '__main__':
    unittest.main()
