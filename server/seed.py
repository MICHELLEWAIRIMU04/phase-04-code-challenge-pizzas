from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

def seed_database():
    # Clear existing data using db.session.query
    db.session.query(RestaurantPizza).delete()
    db.session.query(Restaurant).delete()
    db.session.query(Pizza).delete()

    # Create Restaurants
    restaurants = [
        Restaurant(name="Karen's Pizza Shack", address="address1"),
        Restaurant(name="Sanjay's Pizza", address="address2"),
        Restaurant(name="Kiki's Pizza", address="address3")
    ]
    db.session.add_all(restaurants)
    db.session.commit()

    # Create Pizzas
    pizzas = [
        Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese"),
        Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"),
        Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard")
    ]
    db.session.add_all(pizzas)
    db.session.commit()

    # Create RestaurantPizzas
    restaurant_pizzas = [
        RestaurantPizza(restaurant=restaurants[0], pizza=pizzas[0], price=5),
        RestaurantPizza(restaurant=restaurants[1], pizza=pizzas[1], price=10),
        RestaurantPizza(restaurant=restaurants[2], pizza=pizzas[2], price=15)
    ]
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        seed_database()
        print("Database seeded successfully!")