#!/usr/bin/env python3

from flask import request, session, make_response, jsonify
from flask_restful import Resource

from config import app, db, api
from models import User


class ClearSession(Resource):

    def delete(self):
    
        session['page_views'] = None
        session['user_id'] = None

        return {}, 204

class Signup(Resource):
    
    def post(self):
        json = request.get_json()
        username=json['username']
        password=json['password']

        user = User(
            username=username
        )
        
        user.password_hash = password
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        return user.to_dict(), 201

class CheckSession(Resource):

    def get(self):
        user_id = session.get('user_id')   
        if user_id:
            user = User.query.filter(User.id == user_id).first()
            return user.to_dict(), 200
        else:
            return {}, 204

        

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter(User.username == username).first()

        if user and user.authenticate(password):
            session['user_id'] = user.id
            return make_response(jsonify(user.to_dict()), 200)
        else:
            return {'error': 'Invalid username/password'}, 401

class Logout(Resource):
    def delete(self):
        if session['user_id']:
            session['user_id'] = None
            return {}, 204


api.add_resource(ClearSession, '/clear', endpoint='clear')
api.add_resource(Signup, '/signup', endpoint='signup')
api.add_resource(Login, '/login', endpoint='login')
api.add_resource(Logout, '/logout', endpoint='logout')
api.add_resource(CheckSession, '/check_session', endpoint='check_session')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
