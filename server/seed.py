from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")
    RestaurantPizza.query.delete() 
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address='Karen Hub, Nairobi')
    bistro = Restaurant(name="Sanjay's Pizza", address='Westlands Avenue, Nairobi')
    palace = Restaurant(name="Kiki's Pizza", address='Nyali, Mombasa')
    italiano = Restaurant(name="Mario's Italian Bistro", address='Riverside, Nairobi')
    woodfire = Restaurant(name="WoodFire Pizza", address='Kilimani, Nairobi')
    greenleaf = Restaurant(name="GreenLeaf Vegan Pizza", address='Gigiri, Nairobi')
    
    restaurants = [shack, bistro, palace, italiano, woodfire, greenleaf]

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(name="Geri", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    california = Pizza(name="Melanie", ingredients="Dough, Sauce, Ricotta, Red Peppers, Mustard")
    margherita = Pizza(name="Margherita", ingredients="Dough, Tomato Sauce, Mozzarella, Basil")
    hawaiian = Pizza(name="Hawaiian", ingredients="Dough, Tomato Sauce, Ham, Pineapple")
    bbq = Pizza(name="BBQ Chicken", ingredients="Dough, BBQ Sauce, Chicken, Red Onions, Cilantro")
    vegan_delight = Pizza(name="Vegan Delight", ingredients="Whole Wheat Dough, Hummus, Spinach, Mushrooms, Olives")
    quattro_formaggi = Pizza(name="Quattro Formaggi", ingredients="Dough, Mozzarella, Parmesan, Gorgonzola, Ricotta")

    pizzas = [cheese, pepperoni, california, margherita, hawaiian, bbq, vegan_delight, quattro_formaggi]

    print("Creating RestaurantPizza...")
    restaurant_pizzas = [
        RestaurantPizza(restaurant=shack, pizza=cheese, price=2),
        RestaurantPizza(restaurant=shack, pizza=hawaiian, price=5),
        RestaurantPizza(restaurant=bistro, pizza=pepperoni, price=4),
        RestaurantPizza(restaurant=bistro, pizza=margherita, price=3),
        RestaurantPizza(restaurant=palace, pizza=california, price=5),
        RestaurantPizza(restaurant=italiano, pizza=bbq, price=6),
        RestaurantPizza(restaurant=italiano, pizza=quattro_formaggi, price=7),
        RestaurantPizza(restaurant=woodfire, pizza=cheese, price=4),
        RestaurantPizza(restaurant=woodfire, pizza=vegan_delight, price=8),
        RestaurantPizza(restaurant=greenleaf, pizza=vegan_delight, price=10),
        RestaurantPizza(restaurant=greenleaf, pizza=margherita, price=6),
    ]

    db.session.add_all(restaurants)
    db.session.add_all(pizzas)
    db.session.add_all(restaurant_pizzas)
    db.session.commit()

    print("Seeding done!")