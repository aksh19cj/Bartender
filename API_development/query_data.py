from app import app, db, Drink

with app.app_context():
    drinks = Drink.query.all()
    for drink in drinks:
        print(drink)
