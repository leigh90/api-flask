from flask import Flask, json, request, Response
import flask
from flask.wrappers import Response
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify, dejsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)



class Drink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80),unique=True, nullable=False)
    description = db.Column(db.String(20))

    def __repr__(self):
        return f"{self.name} - {self.description}"
        
books = [
    {
        'id': 1,
        'title': 'Python for Beginners',
    },
    {
        'id': 2,
        'title': 'Web API Mastery',
    },
    {
        'id': 3,
        'title': 'Building Web API',
    },

]


@app.route('/')
def index():
    return 'Hello'

@app.route('/drinks/')
def get_drinks():
    drinks = Drink.query.all()
    print(drinks)
    output = []
    for drink in drinks:
        drink_data = {"name": drink.name, "description": drink.description}
        output.append(drink_data)

    return {'drinks':output}
    # return drink_data

@app.route('/drink/<id>')
def get_drink(id):
    drink = Drink.query.get_or_404(id)
    print(type(drink))
    print(request.json)
    # output = []
    # drinkone = jsonify(drink.name, drink.description)
    # output = output.append(drinkone)
    # return f"drink {output}"
    return jsonify({drink.name:drink.description})
    return ({"name":drink.name, "description":drink.description})


@app.route('/drinks',methods=['POST'])
def add_drink():
    drink = Drink(name=request.json['name'],description=request.json['description'])
    
    db.session.add(drink)
    db.session.commit()
    return {'id':drink.id}

@app.route('/drinks/<id>', methods=["DELETE"])
def delete_drink(id):
    drink = Drink.query.get(id)
    db.session.delete(drink)
    db.session.commit()
    return {'message': "Deleted!"}


@app.route('/books')
def get_books():
    rep = jsonify({'books': books})
    print(type(rep))
    print(rep)
    print(rep.headers)
    print(rep.status_code)
    data = dejsonify

    normal = {'books':books}
 
    return flask.Response(mimetype='application/json')


if __name__ == '__main__':
    app.run(debug=True)