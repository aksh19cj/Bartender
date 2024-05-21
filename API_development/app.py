from flask import Flask,jsonify,request
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.DEBUG)

#set up flask
app = Flask(__name__)

from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class Drink(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(120))

    def __repr__(self):
        return f"{self.name} - {self.description}"


#Creating endpoint
@app.route('/')
#declare a method when someone visits this route
def index():
    return 'Hello!'

#Get drinks
@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    output = []
    for drink in drinks:
        if drink.description == '' or drink.description == None:
            drink_data ={'name':drink.name}
        else:
            drink_data = {'name':drink.name, 'description':drink.description}
        output.append(drink_data)
    return jsonify({"drinks": output}), 200

@app.route('/drinks/<id>', methods=['GET'])
def get_drinks_by_id(id):
    drink = Drink.query.get(id)
    if drink is None:
        return jsonify({'error': 'Drink not found'}), 404
    if drink.description == '' or drink.description == None:
        return jsonify({'name':drink.name})
    return jsonify({'name':drink.name, 'description':drink.description})

@app.route('/drinks/<int:id>', methods=['POST'])
def add_drink_by_id(id):
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({"error": "Name is required"}), 400

    if Drink.query.get(id):
        return jsonify({"error": "Drink with this ID already exists"}), 400

    new_drink = Drink(id=id, name=name, description=description)
    db.session.add(new_drink)
    db.session.commit()

    return jsonify({"message": "Drink added successfully"}), 201

# @app.route('/drinks/<name>', methods=['GET'])
# def get_drinks_by_name(name):
#     # Convert input name to lowercase
#     name = name.lower()
#     print("Lowercase name:", name)  # Print lowercase name for debugging
    
#     # Query the Drink table by the name column
#     drink = Drink.query.filter_by(name=name).first()
#     print("Drink:", drink)  # Print drink for debugging
    
#     # If no drink with the specified name is found, return a 404 error
#     if drink is None:
#         return jsonify({'error': 'Drink not found'}), 404
    
#     # Check if description is empty or None
#     if not drink.description:
#         return jsonify({'name': drink.name})
    
#     # Return the drink details
#     return jsonify({'name': drink.name, 'description': drink.description})

@app.route('/drinks/<name>', methods=['GET'])
def get_drinks_by_name(name):
    drink = Drink.query.get(name)
    logging.debug(f"Drink: {drink}")
    if drink is None:
        logging.warning("Drink not found")
        return jsonify({'error': 'Drink not found'}), 404
    if not drink.description:
        logging.info("Drink found without description")
        return jsonify({'name': drink.name})
    logging.info("Drink found with description")
    return jsonify({'name': drink.name, 'description': drink.description})
