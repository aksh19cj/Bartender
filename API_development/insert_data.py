from app import app, db, Drink

with app.app_context():
    # Create new drink entries
    drink1 = Drink(name='Coke', description='A refreshing soda')
    drink2 = Drink(name='Pepsi', description='Another popular soda')
    drink3 = Drink(name='Fanta', description='A fruity soda')

    # Add the drinks to the session
    db.session.add(drink1)
    db.session.add(drink2)
    db.session.add(drink3)

    # Commit the session to the database
    db.session.commit()

    print("Drinks added successfully.")
