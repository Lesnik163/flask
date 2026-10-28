from flask import Flask, jsonify, request

app = Flask(__name__)

items = [
    {
        "id": 1,
        "name": "Item 1",
        "price": 100
    },
    {
        "id": 2,
        "name": "Item 2",
        "price": 200
    }
]

@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)
@app.route('/items', methods=['POST'])
def create_item():
  data = request.get_json(silent=True) or {}
  name = data.get('name')
  price = data.get('price')
  if not name or price is None:
    return jsonify({'error': 'нужны имя и цена'}), 400

  new_id = max(item['id'] for item in items) + 1 if items else 1
  new_item = {
    'id': new_id,
    'name': name,
    'price': price
  }
  items.append(new_item)
  return jsonify(new_item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
  data = request.get_json(silent=True) or {}
  for item in items:
    if item['id'] == item_id:
      if 'name' in data:
        item['name'] = data['name']
      if 'price' in data:
        item['price'] = data['price']
      return jsonify(item), 200
  return jsonify({'error': 'запись не найдена'}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
  for item in items:
    if item['id'] == item_id:
      items.remove(item)
      return jsonify(item), 200
  return jsonify({'error': 'запись не найдена'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
