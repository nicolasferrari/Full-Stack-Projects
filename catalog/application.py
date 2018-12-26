# -*- coding: utf-8 -*-
import string
import random
import json
import requests
from flask import make_response
import httplib2
from oauth2client.client import FlowExchangeError
from oauth2client.client import flow_from_clientsecrets
from flask import session as login_session
from project_database import Base, Mineral, Item, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
"""
Created on Mon Nov 26 16:33:42 2018

@author: Nicolas
"""

from flask import Flask, render_template, request, redirect,
url_for, flash, jsonify

app = Flask(__name__)


""" Declare my client_id"""

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())[
    'web']['client_id']
engine = create_engine('sqlite:///mineralsitems.db?check_same_thread=False')


Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

"""Create a state token to prevent request forgery
   Store it in the session for later validation"""


@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps(
            'Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 50)
        response.headers['Content-Type'] = 'application/json'
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(json.dumps(
            "Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(json.dumps(
            "Token's client ID does not match app's"), 401)
        print("Token's client ID does not match app's.")
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check to see if user is already logged in
    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps(
            'Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    print(credentials.access_token)
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)
    data = answer.json()
    login_session['username'] = data["name"]
    login_session['picture'] = data["picture"]
    login_session['email'] = data["email"]

    # see if user exists, if it don't make a new one
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome,'
    output += login_session['username']
    output += '!</h1>'

    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height300px;border-radius: 150px;' \
        '-webkit-border-radius:150px;-moz-border-radius: 150px;"> '

    flash("you are now logged in as %s" % login_session["username"])
    print("done!")
    return output

"""logout user"""


@app.route('/logout', methods=['POST'])
def logout():
    # Disconnect based on provider

    if login_session.get('provider') == 'google':
        return gdisconnect()
    else:
        response = make_response(json.dumps({'state': 'notConnected'}),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

""" DISCONNECT - Revoke a current user's token and reset their login_session.
   """


@app.route("/gdisconnect")
def gdisconnect():
    # Only disconnect a connected user.
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps(
            'Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Execute HTTP GET request to revoke current token.
    access_token = credentials.access_token
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        # Reset the user's session.
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        # For whatever reason, the given token was Invalid
        response = make_response(json.dumps('Failed to revoke '
                                 'token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)

""" Shows the different types of minerals """


@app.route('/')
@app.route('/minerals/')
def showMinerals():
    minerals = session.query(Mineral).all()
    return render_template('minerals.html', minerals=minerals)


""" Create a new mineral. For this step is necessary to authenticate first """"


@app.route('/minerals/new/', methods=['GET', 'POST'])
def newMineral():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_mineral = Mineral(name=request.form['name'],
                              user_id=login_session['user_id'])
        session.add(new_mineral)
        session.commit()
        flash('New Mineral Created Successfully')
        return redirect(url_for('showMinerals'))
    else:
        return render_template('NewMineral.html')

""" Edit a Mineral name. This route can be used in order to correct misspelled
 names of minerals or update names."""


@app.route('/minerals/<int:mineral_id>/edit/', methods=['GET', 'POST'])
def editMineral(mineral_id):
    if 'username' not in login_session:
        return redirect('/login')
    edit_mineral = session.query(Mineral).filter_by(id=mineral_id).one()
    if request.method == 'POST':
        if request.form['name']:
            edit_mineral.name = request.form['name']
        session.add(edit_mineral)
        session.commit()
        flash('Mineral edited successfully')
        return redirect(url_for('showItems', mineral_id=mineral_id))
    else:
        return render_template('editmineral.html', mineral_id=mineral_id,
                               i=edit_mineral)

""" Delete a Mineral. This route can be used to delete a
 Mineral that has incorrect name, or a mineral that was added before."""


@app.route('/minerals/<int:mineral_id>/delete/', methods=['GET', 'POST'])
def deleteMineral(mineral_id):
    if 'username' not in login_session:
        return redirect('/login')
    delete_mineral = session.query(Mineral).filter_by(id=mineral_id).one()
    if request.method == 'POST':
        session.delete(delete_mineral)
        session.commit()
        flash('Mineral successfully deleted')
        return redirect(url_for('showMinerals'))
    else:
        return render_template('DeleteMineral.html',
                               mineral_id=mineral_id, i=delete_mineral)

""" Show information of the differents items that belong to a group
    of mineral"""


@app.route('/minerals/<int:mineral_id>/items/')
def showItems(mineral_id):
    mineral = session.query(Mineral).filter_by(id=mineral_id).one()
    items = session.query(Item).filter_by(mineral_id=mineral_id)
    return render_template('items.html', mineral_id=mineral_id,
                           mineral=mineral, items=items)

""" Show item information such as price, origin, colour, description"""


@app.route('/minerals/<int:mineral_id>/items/<int:item_id>/')
def showItemInformation(mineral_id, item_id):
    mineral = session.query(Mineral).filter_by(id=mineral_id).one()
    item = session.query(Item).filter_by(id=item_id)
    return render_template('itemInfo.html', mineral=mineral,
                           mineral_id=mineral_id, item_id=item_id, item=item)

""" Create a new item within a category. Firt authenticate in order to
 proceed with the new item generation"""


@app.route('/minerals/<int:mineral_id>/items/new/', methods=['GET', 'POST'])
def newItem(mineral_id):
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_item = Item(name=request.form['name'],
                        origin=request.form['origin'],
                        colour=request.form['colour'],
                        price=request.form['price'],
                        hardness=request.form['hardness'],
                        description=request.form['description'],
                        mineral_id=mineral_id,
                        user_id=mineral.user_id)
        session.add(new_item)
        session.commit()
        return redirect(url_for('showItems', mineral_id=mineral_id))
    else:
        return render_template('newItem.html', mineral_id=mineral_id)

""" Edit information of the item. The user must be authenticate in the
 web app in order to proceed with the change of item properties."""


@app.route('/minerals/<int:mineral_id>/items/<int:item_id>/edit/',
           methods=['GET', 'POST'])
def editItem(mineral_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    mineral = session.query(Mineral).filter_by(id=mineral_id).one()
    edit_item = session.query(Item).filter_by(id=item_id).one()
    if edit_item.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
         are not authorized to edit this item.\
          Please create your own item in order\
           to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        if request.form['name']:
            edit_item.name = request.form['name']
        session.add(edit_item)
        session.commit()

        if request.form['origin']:
            edit_item.origin = request.form['origin']
        session.add(edit_item)
        session.commit()

        if request.form['colour']:
            edit_item.colour = request.form['colour']
        session.add(edit_item)
        session.commit()

        if request.form['price']:
            edit_item.price = request.form['price']
        session.add(edit_item)
        session.commit()

        if request.form['hardness']:
            edit_item.hardness = request.form['hardness']
        session.add(edit_item)
        session.commit()

        if request.form['description']:
            edit_item.description = request.form['description']
        session.add(edit_item)
        session.commit()

        flash('Item successfully edited')
        return redirect(url_for('showItems', mineral_id=mineral_id,
                                item_id=item_id))
    else:
        return render_template('editItem.html', mineral_id=mineral_id,
                               item_id=item_id, item=edit_item)

""" Delete a specific item. The user must be authenticate in the web app
 in order to remove items within a category."""


@app.route('/minerals/<int:mineral_id>/items/<int:item_id>/delete/',
           methods=['GET', 'POST'])
def deleteItem(mineral_id, item_id):
    if 'username' not in login_session:
        return redirect('/login')
    item_to_delete = session.query(Item).filter_by(id=item_id).one()
    if item_to_delete.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You\
         are not authorized to edit this item.\
          Please create your own item in order\
           to edit.');}</script><body onload='myFunction()'>"
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash('Item Successfully deleted')
        return redirect(url_for('showItems', mineral_id=mineral_id))
    else:
        return render_template('deleteItem.html',
                               mineral_id=mineral_id,  i=item_to_delete)


""" Return serialized information of the list of minerals in the web app"""


@app.route('/minerals/JSON')
def minerals_to_json():
    minerals = session.query(Mineral).all()
    return jsonify(minerals=[i.serialize for i in minerals])

""" Return serialized information of properties of the items within a
 specific group of minerals defined in /minerals route."""


@app.route('/minerals/<int:mineral_id>/items/<int:item_id>/JSON')
def menuitem(mineral_id, item_id):
    minerals = session.query(Mineral).filter_by(id=mineral_id).one()
    item = session.query(Item).filter_by(mineral_id=mineral_id, id=item_id)
    return jsonify(item=[i.serialize for i in item])


def getUserID(email):
    try:
        user = session.query(User).filter_by(email)
        return user.id
    except:
        return None


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
                   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

if __name__ == '__main__':
    app.secret_key = 'supersecretkey'
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=False)
