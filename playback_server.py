from flask import Flask, request
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from bots.commands.playback_alias_command import PlaybackAliasCommand

def setup_server(mumble_client):
    app = Flask(__name__)
    CORS(app)
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["1/second"]
    )

    @app.route('/playback-alias', methods=['POST'])
    @limiter.limit("2/second")
    def playback():
        payload = request.json
        alias_name = payload.get('data', {}).get('alias')    
        cmd = PlaybackAliasCommand(mumble_client, args=[alias_name])
        cmd.execute()
        return 'playback-alias'

    return app