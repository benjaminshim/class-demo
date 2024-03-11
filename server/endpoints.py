"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS

import werkzeug.exceptions as wz

import data.restaurants as restaurants
import data.users as usrs
import data.reviews as rvws
import data.accounts as accs
import data.bars as brs

app = Flask(__name__)
CORS(app)
api = Api(app)

DELETE = 'delete'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to YumYard!"
MAIN_MENU_EP = '/MainMenu'
MENU = 'menu'
USERS_EP = '/users'
USERS_MENU_NM = "User Menu"
USERS_MENU_EP = '/user_menu'
USER_ID = "_id"
RESTAURANTS_EP = '/restaurants'
RESTAURANTS = 'restaurants'
RESTAURANTS_MENU_NM = 'Restaurant Menu'
RESTAURANT_ID = "ID"
REVIEWS_EP = '/reviews'
REVIEWS = 'reviews'
REVIEWS_MENU_NM = 'Reviews Menu'
REVIEWS_ID = 'id'
ACCOUNTS_EP = '/accounts'
ACCOUNTS = 'accounts'
ACCOUNTS_MENU_NM = 'Accounts Menu'
ACCOUNTS_ID = '_ID'
TYPE = 'Type'
DATA = 'DATA'
TITLE = 'Title'
RETURN = 'Return'
BAR_EP = '/bars'
BARS_MENU_NM = 'Bar Menu'
BAR_ID = '_ID'
DEL_RESAURANT_EP = f'{RESTAURANTS_EP}/{DELETE}'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'


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
        Gets the main YumYard menu.
        """
        return {TITLE: MAIN_MENU_NM,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Restaurants'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Reviews'},
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


users_fields = api.model('NewUser', {
    usrs.NAME: fields.String,
    usrs.PASSWORD: fields.Integer,
})


@api.route(f'{USERS_EP}')
class Users(Resource):
    def get(self):
        """
        Get list of all users
        """
        return {
            TYPE: DATA,
            TITLE: 'Current Users',
            DATA: usrs.get_users(),
            MENU: USERS_MENU_NM,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(users_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add a user.
        """
        username = request.json[restaurants.NAME]
        pw = request.json[usrs.PASSWORD]
        try:
            new_id = usrs.add_user(id, username, pw)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_USER_EP}/<name>')
class DelUser(Resource):
    """
    Deletes a User by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self, name):
        """
        Deletes a user.
        """
        try:
            usrs.del_user(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


restaurant_fields = api.model('NewRestaurant', {
    restaurants.TEST_RESTAURANT_NAME: fields.String,
    restaurants.RATING: fields.Integer,
})


@api.route(f'{DEL_RESAURANT_EP}/<name>')
class DelRestaurant(Resource):
    """
    Deletes a restaurant by name.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self, name):
        """
        Deletes a restaurant by name.
        """
        try:
            restaurants.del_restaurant(name)
            return {name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{RESTAURANTS_EP}')
class Restaurants(Resource):
    """
    This class supports various operations on restaurants, such as
    listing them, adding a restaurant, and deleting a restaurant
    """
    def get(self):
        """
        Get list of restaurants and their ratings
        """
        return {TYPE: DATA,
                TITLE: 'Current Restaurants',
                DATA: restaurants.get_restaurants(),
                RETURN: MAIN_MENU_EP,
                }

    @api.expect(restaurant_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add a restaurant.
        """
        # doing requests here, field names should be changed
        name = request.json[restaurants.TEST_RESTAURANT_NAME]
        rating = request.json[restaurants.RATING]
        try:
            new_id = restaurants.add_restaurant(name, rating)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {RESTAURANT_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


review_fields = api.model('NewReview', {
    rvws.RESTAURANT_NAME: fields.String,
    rvws.REVIEW_SENTENCE: fields.String,
})


@api.route(f'{REVIEWS_EP}')
class Reviews(Resource):
    def get(self):
        """
        Get list of all reviews
        """
        return {
            TYPE: DATA,
            TITLE: 'All reviews',
            DATA: rvws.get_reviews(),
            MENU: REVIEWS_MENU_NM,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(review_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add a review.
        """
        name = request.json[rvws.RESTAURANT_NAME]
        review = request.json[rvws.REVIEW_SENTENCE]
        try:
            new_id = rvws.add_review(name, review)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {REVIEWS_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


account_fields = api.model('NewAccount', {
    accs.ACCOUNT_SENTENCE: fields.String,
})


@api.route(f'{ACCOUNTS_EP}')
class Accounts(Resource):
    def get(self):
        """
        Get list of all accounts
        """
        return {
            TYPE: DATA,
            TITLE: 'All accounts',
            DATA: accs.get_accounts(),
            MENU: REVIEWS_MENU_NM,
            RETURN: MAIN_MENU_EP,
        }

    @api.expect(account_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add an account
        """
        account = request.json[accs.ACCOUNT_SENTENCE]
        try:
            new_id = accs.add_account(account)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {ACCOUNTS_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


bar_fields = api.model('NewBar', {
    brs.BAR: fields.String,
    brs.BAR_RATING: fields.Integer,
})


@api.route(f'{BAR_EP}')
class Bars(Resource):
    """
    This class supports various operations on bar, such as
    listing them, adding a bar, and deleting a bar
    """
    def get(self):
        """
        Get list of bars and their ratings
        """
        return {TYPE: DATA,
                TITLE: 'Current Bars',
                DATA: brs.get_bars(),
                MENU: BARS_MENU_NM,
                RETURN: MAIN_MENU_EP,
                }

    @api.expect(bar_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def post(self):
        """
        Add a bar.
        """
        # doing requests here, field names should be changed
        name = request.json[brs.BAR]
        rating = request.json[brs.BAR_RATING]
        try:
            new_id = brs.add_bar(name, rating)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {BAR_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{BAR_EP}/<name>/<rating>')
class Bar_Rating(Resource):
    """
    Updates the rating of a bar.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, name, rating):
        """
        Update the rating of a bar.
        """
        try:
            brs.update_bar_rating(name, rating)
            return {name: 'Updated'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{RESTAURANTS_EP}/<name>/<rating>')
class Rating(Resource):
    """
    Updates the rating of a restaurant.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, name, rating):
        """
        Update the rating of a restaurant.
        """
        try:
            restaurants.update_rating(name, rating)
            return {name: 'Updated'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
