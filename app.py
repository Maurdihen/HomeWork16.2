import datetime as datetime
from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
import json
from datetime import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///HomeWork.db"
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    age = db.Column(db.Integer)
    email = db.Column(db.String)
    role = db.Column(db.String)
    phone = db.Column(db.String)


class Order(db.Model):
    __tablename__ = 'order'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    address = db.Column(db.String)
    price = db.Column(db.Integer)

    customer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Offer(db.Model):
    __tablename__ = 'offers'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    executor_id = db.Column(db.Integer, db.ForeignKey('user.id'))
db.drop_all()
with app.app_context():
    db.create_all()

    with open('data/users.json', 'r', encoding='UTF-8') as users:
        for user in json.load(users):
            usr = User(**user)
            db.session.add(usr)
            db.session.commit()

    with open('data/orders.json', 'r', encoding='UTF-8') as orders:
        for order in json.load(orders):
            order['start_date'] = datetime.strptime(order['start_date'], '%m/%d/%Y')
            order['end_date'] = datetime.strptime(order['end_date'], '%m/%d/%Y')
            ord_ = Order(**order)
            db.session.add(ord_)
            db.session.commit()


    with open('data/offers.json', 'r', encoding='UTF-8') as offers:
        for offer in json.load(offers):
            off = Offer(**offer)
            db.session.add(off)
            db.session.commit()


@app.route('/users', methods=['GET', 'POST'])
def user_page():
    if request.method == 'GET':
        return jsonify([{
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'age': user.age,
                    'email': user.email,
                    'role': user.role,
                    'phone': user.phone
                } for user in db.session.query(User).all()])
    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            new_user = User(**data)
            db.session.add(new_user)
            db.session.commit()
        return 'Completed', 201


@app.route('/users/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def user_by_id(id):
    if request.method == 'GET':
        user = User.query.get(id)
        return jsonify({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'age': user.age,
            'email': user.email,
            'role': user.role,
            'phone': user.phone
        })
    elif request.method == 'PUT':
        # user = User.query.get(id)
        # data = request.json
        # for a in dir(user):
        #     if not a.startswith('__'):
        #         setattr(user, a, data[a])
        # db.session.add(user)
        # db.session.commit()
        # return 'Completed', 201
        user = User.query.get(id)
        data = request.json

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.age = data['age']
        user.email = data['email']
        user.role = data['role']
        user.phone = data['phone']

        db.session.add(user)
        db.session.commit()
        return 'Completed', 201

    elif request.method == 'DELETE':
        user = User.query.get(id)

        db.session.delete(user)
        db.session.commit()
        return 'Removed', 201


@app.route('/offers', methods=['GET', 'POST'])
def offers_page():
    if request.method == 'GET':
        return jsonify([{
                    'order_id': offer.order_id,
                    'executor_id': offer.executor_id
                } for offer in db.session.query(Offer).all()])

    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            new_offer = User(**data)
            db.session.add(new_offer)
            db.session.commit()
        return 'Completed', 201


@app.route('/offers/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def offers_by_id(id):
    offer = Offer.query.get(id)

    if request.method == 'GET':
        return jsonify({
            'order_id': offer.order_id,
            'executor_id': offer.executor_ide
        })

    elif request.method == 'PUT':
        offer = Offer.query.get(id)
        data = request.json
        offer.order_id = data["order_id"]
        offer.executor_id = data["executor_id"]

        db.session.add(offer)
        db.session.commit()
        return 'Removed', 201

    elif request.method == 'DELETE':
        offer = Offer.query.get(id)

        db.session.delete(offer)
        db.session.commit()
        return 'Removed', 201


@app.route('/orders', methods=['GET', 'POST'])
def orders_page():
    if request.method == 'GET':
        return jsonify([{
                    'name': order.name,
                    'description': order.description,
                    'start_date': order.start_date,
                    'end_date': order.end_date,
                    'address': order.address,
                    'price': order.price
                } for order in db.session.query(Order).all()])
    elif request.method == 'POST':
        datas = request.json
        for data in datas:
            new_orders = Order(**data)
            db.session.add(new_orders)
            db.session.commit()
        return 'Completed', 201


@app.route('/orders/<int:id>', methods=['PUT', 'DELETE', 'GET'])
def orders_by_id(id):
    order = Order.query.get(id)

    if request.method == 'GET':
        return jsonify({
            'name': order.name,
            'description': order.description,
            'start_date': order.start_date,
            'end_date': order.end_date,
            'address': order.address,
            'price': order.price
        })

    elif request.method == 'PUT':
        order = Order.query.get(id)
        data = request.json

        order.id = data['id']
        order.name = data["name"]
        order.description = data["description"]
        order.start_date = data['start_date']
        order.end_date = data['end_date']
        order.address = data['address']
        order.price = data['price']
        order.customer_id = data['customer_id']
        order.executor_id = data['executor_id']

        db.session.add(order)
        db.session.commit()
        return 'Removed', 201


if __name__ == '__main__':
    app.run()