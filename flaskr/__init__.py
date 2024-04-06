import os

from flask import Flask, render_template, redirect, url_for, session, request
from boxsdk import OAuth2
from boxsdk import Client

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile('settings.py')


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'


    from werkzeug.security import check_password_hash, generate_password_hash

    #from flaskr.db import get_db

    #bp = Blueprint('auth', __name__, url_prefix='/auth')

    # Create OAuth2 instance
    oauth2 = OAuth2(
        client_id=app.config.get("CLIENT_ID"),
        client_secret=app.config.get("CLIENT_SECRET"),
        store_tokens=None,
    )
    REDIRECT_URI = app.config.get("REDIRECT_URI")


    @app.route('/')
    def home():
        return render_template('index.html')

    @app.route('/box-authenticate')
    def box_authenticate():
        auth_url, csrf_token = oauth2.get_authorization_url(REDIRECT_URI)
        session['csrf_token'] = csrf_token
        return redirect(auth_url)


    # Route to handle Box OAuth callback
    @app.route('/box-auth')
    def box_auth():
        csrf_token = session['csrf_token']
        assert request.args.get('state') == csrf_token
        auth_code = request.args.get('code')
        access_token2, refresh_token = oauth2.authenticate(auth_code)
        client = Client(oauth2)
        access_token = access_token2
        return redirect(url_for('box_content'))

    # Route to display Box content using Box UI elements
    @app.route('/box-content')
    def box_content():
        client = Client(oauth2)
        access_token = oauth2.access_token
        #access_token = oauth2.
        #auth = client.auth().access_token
        root_folder = client.folder(folder_id='0')
        items = root_folder.get_items()
        return render_template('box_content.html', items=items, access_token=access_token)

    #from . import auth
    #app.register_blueprint(auth.bp)
    return app

