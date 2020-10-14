import os
import requests
from werkzeug.datastructures import Headers
from flask import Flask, request, jsonify, redirect, url_for, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from flask_httpauth import HTTPBasicAuth
from flask_jwt_extended import JWTManager, jwt_required, jwt_optional, create_access_token, get_jwt_identity

from bots.commands.playback_alias_command import PlaybackAliasCommand

class User:
    def __init__(self):
        self.id = 1
        self.username = os.environ["APP_USERNAME"]
        self.password = os.environ["APP_PASSWORD"]

def setup_server(mumble_client):
    app = Flask(__name__, static_folder='./build', static_url_path='/')
    app.config['SECRET_KEY'] = os.environ["APP_SECRET_KEY"]
    jwt = JWTManager(app)
    auth = HTTPBasicAuth()
    CORS(app)

    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["2/second"]
    )

    @auth.verify_password
    def authenticate(username, password):
        user = User()
        if username == user.username and password == user.password:
            return user

    @app.route('/login', methods=['GET','POST'])
    # @auth.login_required()
    def login():
        current_user = auth.current_user()
        username = current_user.username

        access_token = create_access_token(identity=username)
        return redirect(url_for('index', token=access_token))

    @app.route('/')
    # @jwt_optional
    def index():
        # if not get_jwt_identity():
        #     return jsonify({"error": "Missing token"}), 401
        return app.send_static_file('index.html')
    app.add_url_rule('/', 'index', index)

    @app.route('/playback-alias', methods=['POST'])
    # @jwt_required
    @limiter.limit("2/second")
    def playback():
        payload = request.json
        alias_name = payload.get('data', {}).get('alias')    
        cmd = PlaybackAliasCommand(mumble_client, args=[alias_name])
        cmd.execute()
        return 'playback-alias'

    @app.route('/graphql', methods=['POST'])
    def graphql():
        return requests.post(
            'http://host.docker.internal:8080/v1/graphql',
            headers={
                'content-type': 'application/json',
                'x-hasura-admin-secret': 'nutsnack'
            },
            data=request.data).text

    return app