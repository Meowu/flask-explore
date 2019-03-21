from flask import request
from flask_restplus import Resource

from ..util.dto import UserDto
from ..service.user_service import save_new_user, get_a_user, get_all_users, delete_a_user, put_a_user

api = UserDto.api
_user = UserDto.user

@api.route('/')
class UserList(Resource):

    @api.doc('list_of_registered_users')
    @api.marshal_list_with(_user, envelope='data')
    def get(self):
        """List all registered users"""
        return get_all_users()

    @api.response(201, 'User successfully created.')
    @api.doc('create a new user')
    @api.expect(_user, validate=True)
    def post(self):
        """Creates a new User"""
        data = request.json
        result = save_new_user(data=data)
        print('post', result)
        return result

@api.route('/<public_id>')
@api.param('public_id', 'The User identifier')
@api.response(404, 'User not found.')
class User(Resource):
    @api.doc('get a user')
    @api.marshal_with(_user)
    def get(self, public_id):
        """get a user given its identifier"""
        user = get_a_user(public_id)
        print('user', user, public_id)
        if not user:
            api.abort(404)
        else:
            return user

    @api.doc('delete a user')
    # @api.marshal_with(_user) # if not comment out this, it will result user with each prop of null.
    def delete(self, public_id):
        """delete a user with its identifier"""
        res = delete_a_user(public_id)
        if not res:
            api.abort(404)
        else:
            return res

    @api.response(200, 'Successfully changed.')
    @api.doc('put a user')
    @api.expect(_user, validate=True)
    def put(self, public_id):  # 在该接口中，如何保证提交的 json 数据和 model 一致，并且安全地修改 session 的信息。
        """post a user information"""
        data = request.json
        print('put val', data)
        return put_a_user(public_id, data)