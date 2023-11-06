"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import Flask
from flask_restx import Resource, Api
# import db.db as db
import data.customers as cstmrs

app = Flask(__name__)
api = Api(app)

MAIN_MENU = 'MainMenu'
MAIN_MENU_NM = "Welcome to Text Game!"
HELLO_EP = '/hello'
HELLO_RESP = 'hello'
CUSTOMERS_EP = '/customers'
CUSTOMERS = 'customers'
CUSTOMER_MENU_NM = "Costumer Menu"
RESTAURANTS_EP = '/restaurants'
RESTAURANTS = 'restaurants'
TYPE = 'Type'
DATA = 'DATA'
TITLE = 'Title'


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


@api.route(f'/{MAIN_MENU}')
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
                    '3': {'url': f'{CUSTOMERS_EP}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'{CUSTOMERS_EP}')
class Customers(Resource):
    def get(self):
        return {TYPE: DATA,
                TITLE: 'Current Customers',
                DATA: cstmrs.get_customers(),
                MENU: CUSTOMER_MENU_EP,
                RETURN: MAIN_MENU_EP,
                }


@api.route(f'{RESTAURANTS_EP}')
class Restaurants(Resource):
    def get(self):
        return {TYPE: DATA,
                TITLE: 'Current Restaurants',
                DATA:
                    {"Wakuriya":
                        {
                            "city": 'San Francisco',
                            "state": 'California',
                            "price": '$$$$'
                        },
                        "Nico":
                        {
                            "city": 'San Francisco',
                            "state": 'California',
                            "price": '$$$'
                        },
                        "Huge Thai":
                        {
                            "city": 'New York',
                            "state": 'New York',
                            "price": '$$'
                        }
                     }
                }
