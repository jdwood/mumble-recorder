import os
import requests
from flask import Flask, request, jsonify, redirect, url_for, Response
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from bots.commands.playback_alias_command import PlaybackAliasCommand

def setup_server(mumble_client):
    app = Flask(__name__, static_folder='./build', static_url_path='/')
    CORS(app)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["2/second"]
    )

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/playback-alias', methods=['POST'])
    @limiter.limit("2/second")
    def playback():
        payload = request.json
        alias_name = payload.get('data', {}).get('alias')    
        cmd = PlaybackAliasCommand(mumble_client, args=[alias_name])
        cmd.execute()
        return jsonify({"success": True})

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