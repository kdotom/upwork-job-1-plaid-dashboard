from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user

import jsonpickle

from . import db
from . import client, api_client

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)

@main.route('/link_account')
@login_required
def link_account():
    return render_template('link_account.html')

@main.route("/create_link_token", methods=['POST'])
@login_required
def create_link_token():
    # Get the client_user_id by searching for the current user
    client_user_id = str(current_user.id)
    # Create a link_token for the given user
    request = LinkTokenCreateRequest(
            products=[Products("auth")],
            client_name="Plaid Dashboard",
            country_codes=[CountryCode('US')],
            language='en',
            user=LinkTokenCreateRequestUser(
                client_user_id=client_user_id
            )
        )
    response = client.link_token_create(request)
    # Send the data to the client
    return jsonify(response.to_dict())

access_token = None
item_id = None

@main.route('/exchange_public_token', methods=['POST'])
@login_required
def exchange_public_token():
    global access_token, request
    public_token = request.form['public_token']
    request = ItemPublicTokenExchangeRequest(
      public_token=public_token
    )
    response = client.item_public_token_exchange(request)

    # These values should be saved to a persistent database and
    # associated with the currently signed-in user
    access_token = response['access_token']
    item_id = response['item_id']

    return jsonify({'public_token_exchange': 'complete'})

@main.route('/accounts_balance_get', methods=['GET'])
@login_required
def accounts_balance_get():
    global access_token
    # Pull real-time balance information for each account associated
    # with the Item
    request = AccountsBalanceGetRequest(access_token=access_token)
    response = client.accounts_balance_get(request)
    accounts = response['accounts']

    return jsonpickle.encode(accounts)