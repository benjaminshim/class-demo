"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import Flask, jsonify, request
from flask_restx import Resource, Api, fields
from flask_cors import CORS

import werkzeug.exceptions as wz
import sys

import data.restaurants as restaurants
import data.users as usrs
import data.reviews as rvws
import forms.restaurant_form as rst

app = Flask(__name__)
CORS(app)
api = Api(app)

DELETE = 'delete'
MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome!"
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
# Have to check this later not sure if correct the logins
LOGIN_FORM = 'login'
LOGIN_FORM_EP = f'{USERS_EP}/{LOGIN_FORM}'
# Instead maybe have a form so we can choose state of restaurants
RESTAURANT_FORM = 'state'
RESTAURANT_FORM_EP = f'{RESTAURANTS_EP}/{RESTAURANT_FORM}'
TYPE = 'Type'
DATA = 'DATA'
TITLE = 'Title'
RETURN = 'Return'
DEL_RESTAURANT_EP = f'{RESTAURANTS_EP}/{DELETE}'
DEL_USER_EP = f'{USERS_EP}/{DELETE}'
DEL_REVIEW_EP = f'{REVIEWS_EP}/{DELETE}'


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
        Gets the main menu.
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
    usrs.FIRST_NAME: fields.String,
    usrs.LAST_NAME: fields.String,
    usrs.EMAIL: fields.String,
    usrs.PASSWORD: fields.String,
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
        first_name = request.json[usrs.FIRST_NAME]
        last_name = request.json[usrs.LAST_NAME]
        email = request.json[usrs.EMAIL]
        password = request.json[usrs.PASSWORD]

        try:
            new_id = usrs.add_user(first_name, last_name, email, password)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {USER_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{DEL_USER_EP}/<user_id>')
class DelUser(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self, user_id):
        """
        Deletes a user.
        """
        try:
            usrs.del_user(user_id)
            return {'Deleted user with User ID':
                    f'{user_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{USERS_EP}/<user_id>/<new_email>')
class UpdateEmail(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, user_id, new_email):
        """
        Update the email of a user.
        """
        try:
            if not usrs.update_email(user_id, new_email):
                raise wz.NotFound(f'User with ID'
                                  f'{user_id} not found')
            return {'Updated email with User ID': f'{user_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


# Restaurants
restaurant_fields = api.model('NewRestaurant', {
    restaurants.NAME: fields.String,
    restaurants.RESTAURANT_TYPE: fields.String,
    restaurants.DESCRIPTION: fields.String,
    restaurants.ADDRESS: fields.String,
    restaurants.CITY: fields.String,
    restaurants.STATE: fields.String,
    restaurants.ZIP_CODE: fields.String,
})


@api.route(f'{RESTAURANTS_EP}/<restaurant_id>')
class UpdateRestaurant(Resource):
    @api.doc(params={'restaurant_id': 'The unique ID of the restaurant'})
    @api.expect(restaurant_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, restaurant_id):
        """
        Update a restaurant using its unique 24 character ID.
        """
        updated_data = request.json
        try:
            if not restaurants.update_restaurant(restaurant_id, updated_data):
                raise wz.NotFound(f'Restaurant with ID'
                                  f'{restaurant_id} not found')
            return {'Updated restaurant with Restaurant ID':
                    f'{restaurant_id}'}
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')


@api.route(f'{DEL_RESTAURANT_EP}/<restaurant_id>')
class DelRestaurant(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self, restaurant_id):
        """
        Delete a restaurant using its unique 24 character ID.
        """
        try:
            restaurants.del_restaurant(restaurant_id)
            return {'Deleted restaurant with Restaurant ID':
                    f'{restaurant_id}'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{DEL_RESTAURANT_EP}')
class DelAllRestaurants(Resource):
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self):
        """
        Delete all restaurants.
        """
        try:
            count = restaurants.delete_all()
            return f'All {count} restaurants have been deleted.'
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
        Get a list of all restaurants.
        """
        # Get the state from the query parameters
        state = request.args.get('state')
        if state:
            # If state is provided in query, filter restaurants by the state
            filtered_restaurants = restaurants.get_restaurants_by_state(state)
            return {
                TYPE: DATA,
                TITLE: f'Restaurants in {state}',
                DATA: filtered_restaurants,
            }
        else:
            # If no state is provided, return all restaurants
            all_restaurants = restaurants.get_restaurants()
            return {
                TYPE: DATA,
                TITLE: 'Current Restaurants',
                DATA: all_restaurants,
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
        name = request.json[restaurants.NAME]
        restaurant_type = request.json[restaurants.RESTAURANT_TYPE]
        description = request.json[restaurants.DESCRIPTION]
        address = request.json[restaurants.ADDRESS]
        city = request.json[restaurants.CITY]
        state = request.json[restaurants.STATE]
        zip_code = request.json[restaurants.ZIP_CODE]
        try:
            new_id = restaurants.add_restaurant(name, restaurant_type,
                                                description, address,
                                                city, state, zip_code)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {RESTAURANT_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


review_fields = api.model('NewReview', {
    rvws.USER_ID: fields.Integer,
    rvws.RESTAURANT_ID: fields.Integer,
    rvws.REVIEW_SENTENCE: fields.String,
    rvws.RATING: fields.Integer
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
        review = request.json[rvws.REVIEW_SENTENCE]
        rating = request.json[rvws.RATING]
        user = request.json[rvws.USER_ID]
        restaurant = request.json[rvws.RESTAURANT_ID]

        try:
            new_id = rvws.add_review(user, restaurant, review, rating)
            if new_id is None:
                raise wz.ServiceUnavailable('We have a technical problem.')
            return {REVIEWS_ID: new_id}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


@api.route(f'{REVIEWS_EP}/<user_id>/<restaurant_id>/<review>/<rating>')
class UpdateReview(Resource):
    """
    Updates the review of a restaurant.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def put(self, user_id, restaurant_id, review, rating):
        """
        Updates the review of a restaurant.
        """
        try:
            rvws.update_review(int(user_id), int(restaurant_id),
                               review, int(rating))
            return {review: 'Updated'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{DEL_REVIEW_EP}/<user_id>/<restaurant_id>')
class DelReview(Resource):
    """
    Deletes a Review.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    @api.response(HTTPStatus.SERVICE_UNAVAILABLE,
                  'We have a technical problem.')
    def delete(self, user_id, restaurant_id):
        """
        Deletes a review.
        """
        try:
            rvws.del_review(int(user_id), int(restaurant_id))
            return 'Review Deleted'
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


@api.route(f'{RESTAURANT_FORM_EP}')
class RestaurantForm(Resource):
    """
    Get the form to find restaurant by state
    """
    def get(self):
        """
        Get the form to find restaurant by state
        """
        # Change name of login form to restaurant state
        form_data = rst.get_form()
        return form_data, 200  # Return as JSON response


@api.route('/sample_data')
class SampleData(Resource):
    def get(self):
        """
        Get sample data for testing or development.
        """
        sample_data = {
            'users': [
                {'first_name': 'John', 'last_name': 'Doe', 'email': 'john.doe@example.com', 'password': 'password123'},
                {'first_name': 'Alice', 'last_name': 'Smith', 'email': 'alice.smith@example.com', 'password': 'password456'},
                {'first_name': 'Bob', 'last_name': 'Johnson', 'email': 'bob.johnson@example.com', 'password': 'password789'}
            ],
            'restaurants': [
                {'name': 'Delicious Bites', 'restaurant_type': 'Italian', 'description': 'A cozy Italian restaurant with a wide selection of pasta dishes.', 'address': '123 Main Street', 'city': 'New York', 'state': 'NY', 'zip_code': '10001'},
                {'name': 'Taco Haven', 'restaurant_type': 'Mexican', 'description': 'Authentic Mexican cuisine with flavorful tacos and burritos.', 'address': '456 Oak Avenue', 'city': 'Los Angeles', 'state': 'CA', 'zip_code': '90001'},
                {'name': 'Spice Kingdom', 'restaurant_type': 'Indian', 'description': 'Experience the rich flavors of Indian spices in every dish.', 'address': '789 Elm Street', 'city': 'Chicago', 'state': 'IL', 'zip_code': '60001'}
            ],
            'reviews': [
                {'user_id': '1', 'restaurant_id': '1', 'review_sentence': 'Great food and friendly service!', 'rating': 4},
                {'user_id': '2', 'restaurant_id': '2', 'review_sentence': 'Delicious tacos and quick service!', 'rating': 5},
                {'user_id': '3', 'restaurant_id': '3', 'review_sentence': 'Amazing Indian food with excellent ambiance.', 'rating': 3}
            ]
        }
        return sample_data
