from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from models import db, Restaurant, Pizza, RestaurantPizza

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)

# Basic route to verify app is working
@app.route('/')
def home():
    return "Pizza Restaurants API is running!", 200

# GET /restaurants
@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    try:
        restaurants = Restaurant.query.all()
        return jsonify([{
            'id': restaurant.id, 
            'name': restaurant.name, 
            'address': restaurant.address
        } for restaurant in restaurants]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# GET /restaurants/<id>
@app.route('/restaurants/<int:id>', methods=['GET'])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    return jsonify({
        'id': restaurant.id,
        'name': restaurant.name,
        'address': restaurant.address,
        'restaurant_pizzas': [
            {
                'id': rp.id,
                'pizza_id': rp.pizza_id,
                'restaurant_id': rp.restaurant_id,
                'price': rp.price,
                'pizza': {
                    'id': rp.pizza.id,
                    'name': rp.pizza.name,
                    'ingredients': rp.pizza.ingredients
                }
            } for rp in restaurant.restaurant_pizzas
        ]
    }), 200

# DELETE /restaurants/<id>
@app.route('/restaurants/<int:id>', methods=['DELETE'])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return jsonify({"error": "Restaurant not found"}), 404
    
    db.session.delete(restaurant)
    db.session.commit()
    return '', 204

# GET /pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        'id': pizza.id,
        'name': pizza.name,
        'ingredients': pizza.ingredients
    } for pizza in pizzas]), 200

# POST /restaurant_pizzas
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()

    # Validate pizza and restaurant exist
    pizza = Pizza.query.get(data.get('pizza_id'))
    restaurant = Restaurant.query.get(data.get('restaurant_id'))
    
    if not pizza or not restaurant:
        return jsonify({"errors": ["validation errors"]}), 400

    try:
        # Create RestaurantPizza with price validation
        restaurant_pizza = RestaurantPizza(
            price=data.get('price'),
            pizza_id=data.get('pizza_id'),
            restaurant_id=data.get('restaurant_id')
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        return jsonify({
            'id': restaurant_pizza.id,
            'pizza_id': restaurant_pizza.pizza_id,
            'restaurant_id': restaurant_pizza.restaurant_id,
            'price': restaurant_pizza.price,
            'pizza': {
                'id': restaurant_pizza.pizza.id,
                'name': restaurant_pizza.pizza.name,
                'ingredients': restaurant_pizza.pizza.ingredients
            },
            'restaurant': {
                'id': restaurant_pizza.restaurant.id,
                'name': restaurant_pizza.restaurant.name,
                'address': restaurant_pizza.restaurant.address
            }
        }), 201
    
    except ValueError:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400
    except Exception:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 422

if __name__ == '__main__':
    app.run(port=5555, debug=True)