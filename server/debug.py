from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

def debug_database():
    with app.app_context():
        # Print all Restaurants
        print("Restaurants:")
        restaurants = Restaurant.query.all()
        for restaurant in restaurants:
            print(f"ID: {restaurant.id}, Name: {restaurant.name}, Address: {restaurant.address}")
        
        # Print all Pizzas
        print("\nPizzas:")
        pizzas = Pizza.query.all()
        for pizza in pizzas:
            print(f"ID: {pizza.id}, Name: {pizza.name}, Ingredients: {pizza.ingredients}")
        
        # Print all RestaurantPizzas
        print("\nRestaurant Pizzas:")
        restaurant_pizzas = RestaurantPizza.query.all()
        for rp in restaurant_pizzas:
            print(f"ID: {rp.id}, Restaurant: {rp.restaurant.name}, Pizza: {rp.pizza.name}, Price: {rp.price}")

if __name__ == '__main__':
    debug_database()