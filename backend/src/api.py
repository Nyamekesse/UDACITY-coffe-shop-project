# from crypt import methods
import os
from turtle import title
from flask import Flask, request, jsonify, abort
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@TODO uncomment the following line to initialize the database
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
!! Running this function will add one
'''
# db_drop_and_create_all()

# ROUTES
'''
@TODO implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    try:
        available_drinks = Drink.query.order_by(Drink.id).all()
        if(len(available_drinks) == 0):
            abort(404)
        else:
            drinks = available_drinks.short()
            return jsonify({
                'success': True,
                'drinks': drinks
            })

    except:
        abort(404)


'''
@TODO implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


# @requires_auth('get:drinks-detail')
@app.route('/drinks-detail', methods=['GET'])
def get_drink_details():
    try:
        available_drinks = Drink.query.order_by(Drink.id).all()
        if(len(available_drinks) == 0):
            abort(404)
        else:
            drinks = available_drinks.long()
            return jsonify({
                'success': True,
                'drinks': drinks
            })

    except:
        abort(404)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''


# @requires_auth('post:drinks')
@app.route('/drinks', methods=['POST'])
def add_new_drink():
    body = request.get_json()
    if body == None:
        abort(422)
    else:
        try:
            drink = Drink(title=body.get('title'), recipe=body.get('recipe'))
            drink.add()
            return jsonify({
                'success': True,
                'drink': drink.long()
            })
        except:
            abort(401)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''


# @requires_auth('patch:drinks')
@app.route('/drinks/<int:id>', methods=['PATCH'])
def update_drinks(id):
    body = request.get_json()
    if body == None:
        abort(422)
    else:
        try:
            drink = Drink.query.filter_by(Drink.id == id).one_or_none()
            if drink == None:
                abort(404)
            drink.title = body.get('title')
            drink.recipe = body.get('recipe')
            drink.update()
            return jsonify({
                'success': True,
                'drinks': drink.long()
            })
        except:
            abort(401)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


# @requires_auth('delete:drinks')
@app.route('/drinks/<int:id>', methods=['DELETE'])
def delete_drink(id):
    try:
        drink = Drink.query.filter_by(Drink.id == id).one_or_none()
        drink.delete()
        return jsonify({
            'success': True,
            'delete': id
        })
    except:
        abort(404)


# Error Handling


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@app.errorhandler(401)
def unauthorized(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": "unauthorized"
    }), 401


@app.errorhandler(403)
def forbidden(error):
    return jsonify({
        "success": False,
        "error": 403,
        "message": "forbidden"
    }), 403
