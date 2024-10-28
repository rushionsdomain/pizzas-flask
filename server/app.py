from models import db, Restaurant, RestaurantPizza, Pizza
from flask_migrate import Migrate
from flask import Flask, request, jsonify, make_response
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

@app.route('/')
def index():
    return '<h1>Code challenge</h1>'

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([restaurant.to_dict(only=('id', 'name', 'address')) for restaurant in restaurants])

@app.route('/restaurants', methods=['POST'])
def create_restaurant():
    data = request.get_json()

    if not data:
        return make_response(jsonify({"error": "Request must be JSON"}), 400)

    required_fields = ['name', 'address']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({"error": f"{field} is required"}), 400)

    try:
        restaurant = Restaurant(
            name=data['name'],
            address=data['address']
        )
        db.session.add(restaurant)
        db.session.commit()

        return jsonify(restaurant.to_dict(only=('id', 'name', 'address'))), 201

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        return jsonify(restaurant.to_dict(only=('id', 'name', 'address', 'restaurant_pizzas')))
    return make_response(jsonify({"error": "Restaurant not found"}), 404)

@app.route('/restaurants', methods=['DELETE'])
def delete_restaurants():
    db.session.query(Restaurant).delete()
    db.session.commit()
    return make_response("", 204)

@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return make_response("", 204)
    return make_response(jsonify({"error": "Restaurant not found"}), 404)

@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([pizza.to_dict(only=('id', 'name', 'ingredients')) for pizza in pizzas])

@app.route('/pizzas/<int:id>', methods=['GET'])
def get_pizza(id):
    pizza = Pizza.query.get(id)
    if pizza:
        return jsonify(pizza.to_dict(only=('id', 'name', 'ingredients')))
    return make_response(jsonify({"error": "Pizza not found"}), 404)

@app.route('/pizzas', methods=['POST'])
def create_pizza():
    data = request.get_json()

    if not data:
        return make_response(jsonify({"error": "Request must be JSON"}), 400)

    required_fields = ['name', 'ingredients']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({"error": f"{field} is required"}), 400)

    try:
        pizza = Pizza(
            name=data['name'],
            ingredients=data['ingredients']
        )
        db.session.add(pizza)
        db.session.commit()

        return jsonify(pizza.to_dict(only=('id', 'name', 'ingredients'))), 201

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/pizzas', methods=['DELETE'])
def delete_pizzas():
    db.session.query(Pizza).delete()
    db.session.commit()
    return make_response("", 204)

@app.route('/restaurant_pizzas', methods=['GET'])
def get_restaurant_pizzas():
    restaurant_pizzas = RestaurantPizza.query.all()
    return jsonify([restaurant_pizza.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id')) for restaurant_pizza in restaurant_pizzas])

@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    
    if not data:
        return make_response(jsonify({"error": "Request must be JSON"}), 400)
    
    required_fields = ['price', 'pizza_id', 'restaurant_id']
    for field in required_fields:
        if field not in data:
            return make_response(jsonify({"error": f"{field} is required"}), 400)

    try:
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        return jsonify(restaurant_pizza.to_dict(only=('id', 'price', 'pizza_id', 'restaurant_id'))), 201

    except Exception as e:
        return make_response(jsonify({"error": str(e)}), 400)

@app.route('/restaurant_pizzas', methods=['DELETE'])
def delete_restaurant_pizzas():
    db.session.query(RestaurantPizza).delete()
    db.session.commit()
    return make_response("", 204)

with app.app_context():
    print("Available routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

if __name__ == '__main__':
    app.run(port=5555, debug=True)