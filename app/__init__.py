from flask import Flask
from flask_restx import Api
from werkzeug.middleware.proxy_fix import ProxyFix
from app.controllers.board_controller import api as board_api


def create_app():
    # app init
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    api = Api(
        app, version='0.1',
        title='Board API'
    )

    # namesapces
    api.add_namespace(board_api)

    return app
