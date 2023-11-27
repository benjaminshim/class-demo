"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields

import werkzeug.exceptions as wz

import data.db as db
# import data.users as usrs
# import data.customers as cstmrs

app = Flask(__name__)
api = Api(app)

DELETE = 'delete'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Text Game!"
MAIN_MENU_EP = '/MainMenu'
MENU = 'menu'
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
USERS_EP = '/users'
USERS_MENU_NM = "User Menu"
USERS_MENU_EP = '/user_menu'
RESTAURANTS_EP = '/db'
RESTAURANTS = 'restaurants'
RESTAURANT_ID = "ID"
TYPE = 'Type'
DATA = 'DATA'
TITLE = 'Title'
DEL_RESAURANT_EP = f'{RESTAURANTS_EP}/{DELETE}'
# RETURN = 'Return'


@api.route(HELLO_EP)
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {HELLO_RESP: 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'/{MAIN_MENU_EP}')
# @api.route('/')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {TITLE: MAIN_MENU_NM,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Games'},
                    '3': {'url': f'{USERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{USERS_MENU_EP}')
class UserMenu(Resource):
    """
    This will deliver our user menu.
    """
    def get(self):
        """
        Gets the user menu.
        """
        return {
                   TITLE: USERS_MENU_NM,
                   'Default': '0',
                   'Choices': {
                       '1': {
                            'url': '/',
                            'method': 'get',
                            'text': 'Get User Details',
                       },
                       '0': {
                            'text': 'Return',
                       },
                   },
               }


@api.route(f'{USERS_EP}')
class Users(Resource):
    def get(self):
        return {TYPE: DATA,
                TITLE: 'Current Customers',
                DATA:
                    {"Andy":
                        {
                            "joined": '12/17/2022'
                        },
                        "Benjamin":
                        {
                            "joined": '04/30/2022'
                        },
                        "Carolina":
                        {
                            "joined": '11/05/2022'
                        },
                        "Bridget":
                        {
                            "joined": '03/12/2022'
                        }
                     }
                }


restaurant_fields = api.model('NewRestaurant', {
    db.TEST_RESTAURANT_NAME: fields.String,
    db.RATING: fields.Integer,
})


@api.route(f'{DEL_RESAURANT_EP}/<name>')
class DelRestaurant(Resource):
    """
    Deletes a restaurant by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, name):
        """
        Deletes a restaurant by name.
        """
        try:
            db.del_restaurant(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{RESTAURANTS_EP}')
class Restaurants(Resource):
    def get(self):
        return {TYPE: DATA,
                TITLE: 'Current Restaurants',
                DATA: db.get_restaurants(),
                }

    @api.expect(restaurant_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add a game.
        """
        name = request.json[db.TEST_RESTAURANT_NAME]
        rating = request.json[db.RATING]
        try:
            new_id = db.add_restaurant(name, rating)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {RESTAURANT_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
