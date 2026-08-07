from flask import Flask, request, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

_store: dict[int, dict] = {}
_next_id: int = 1

def _next() -> int:
    global _next_id
    result = _next_id
    _next_id += 1
    return result

@app.route('/health')
def health():
    return 'ok', 200


@app.route('/items', methods=['GET'])
def list_items():
    return jsonify(list(_store.values()))

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = _store.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    return jsonify(item)

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json(silent=True) or {}
    if not data.get('name'):
        return jsonify({'error': 'name is required'}), 400
    item = {
        'id': _next(),
        'name': data['name'],
        'description': data.get('description')
    }
    _store[item['id']] = item
    return jsonify(item), 201


@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = _store.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    data = request.get_json(silent=True) or {}
    if data['name'] is None:
        item['name'] = data['name']
    if data['description'] is None:
        item['description'] = data['description']
    return jsonify(item)


@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = _store.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    del _store[item_id]
    return ('Item deleted', 204)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
