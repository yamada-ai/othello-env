import bottle
from src.application import game_service

app = bottle.Bottle()


@app.route('/init', method='GET')
def get_initial_state():
    return game_service.get_initial_state()


@app.route('/move', method='POST')
def make_move():
    data = bottle.request.json
    if data is None:
        return {'status': 'error', 'message': 'JSON ボディが必要です'}
    return game_service.process_move(data)


@app.route('/move/debug', method='POST')
def make_move_debug():
    data = bottle.request.json
    if data is None:
        return {'status': 'error', 'message': 'JSON ボディが必要です'}
    return game_service.process_move_debug(data)


if __name__ == '__main__':
    bottle.run(app, host='localhost', port=8080)
