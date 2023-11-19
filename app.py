from flask import Flask, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
import os


app = Flask('__name__')
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': id, 'username': self.username, 'email': self.email}
    
db.create_all()


# Что-то вроде домашней страницы
@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify({"message": "test route"}), 200)


# Создание пользователя
@app.route('/users', methods=['POST'])
def create_user(): 
    try:
        data = request.get_json()
        new_user = User(username=data.get('username'), email=data.get('email'))
        db.session.add(new_user)
        db.session.commit()
        return make_response(jsonify({'message': 'user has been created'}), 500)
    except Exception:
        return make_response(jsonify({'message': 'error create user'}), 401)
    

# Получение всех пользователей
@app.route('/users', method=['GET'])
def get_users():
    try:
        users = User.objects.all()
        return make_response(jsonify({'users': [user.json() for user in users]}), 200)
    except Exception:
        return make_response(jsonify({'message': "error getting users"}), 500)
    

# Получение пользователя по id
@app.route('/users/<int:id>', method=['GET'])
def get_users(id):
    try:
        user = User.objects.filter_by(id=id).first()
        if user:    
            return make_response(jsonify({'users': user.json()}), 200)
        return  make_response(jsonify({'message': 'user not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': "error getting user"}), 500)
    

# Обновление пользователя
@app.route('/users/<int:id>', method=['PUT'])
def update_user(id):
    try:
        user = User.objects.filter_by(id=id).first()
        if user:
            data = request.get_json()
            user.username = data['username']
            user.email = data['email']
            db.session.commit()
            return make_response(jsonify({'message': 'successeful update user'}), 200)
        return  make_response(jsonify({'message': 'user not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': "error update user"}), 500)


# Удаление пользователя
@app.route('/users/<int:id>', method=['DELETE'])
def update_user(id):
    try:
        user = User.objects.filter_by(id=id).first()
        if user:
            db.session.delete()
            db.session.commit()
            return make_response(jsonify({'message': 'user has been deleted'}), 200)
        return  make_response(jsonify({'message': 'user not found'}), 404)
    except Exception:
        return make_response(jsonify({'message': "error deleting user"}), 500)