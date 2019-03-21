import uuid
import datetime

from app.main import db
from app.main.model.user import User


def save_new_user(data):

    user = User.query.filter_by(email=data['email']).first()
    if not user:
        new_user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password=data['password'],
            registered_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in'
        }
        return response_object, 409


def get_all_users():
    return User.query.all()


def get_a_user(id):
    return User.query.filter_by(public_id=id).first()

def delete_a_user(id):
    user = User.query.filter_by(public_id=id).first()
    if not user:
        return None
    else:
        db.session.delete(user)
        db.session.commit()
        response_object = {
            'status': 'success',
            'code': 0,
            'message': 'Successfully deleted.'
        }
        return response_object, 200

def put_a_user(id, data):
    user = User.query.filter_by(public_id=id).first()
    if not user:
        res_object = {
            'status': 'fail',
            'code': 1,
            'message': 'User not exists.'
        }
        return res_object, 404
    else:
        print('data enum', enumerate(data))
        # for val, key in enumerate(data):
        #     user[key] = val
        user.username = 'Meowu'
        # user.update({'name': 'CCC'})
        db.session.commit()
        res_object = {
            'status': 'success',
            'code': 0,
            'message': 'Successfully modified.'
        }
        return res_object, 200

def save_changes(data):
    db.session.add(data)
    db.session.commit()
