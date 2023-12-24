"""Flask App for Flask Cafe."""

import os

from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension

import routes_auth
import routes_cafes
import routes_home
import routes_users
import routes_likes_api

from models import connect_db, bcrypt

def create_app(**config):
    """Set up and return Flask app (pass kwargs to override default config)."""

    app = Flask(__name__, root_path=".")
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.environ.get(
            "DATABASE_URL", 'postgresql:///flask_cafe'),
        SQLALCHEMY_ECHO=True,
        SECRET_KEY= os.environ.get("FLASK_SECRET_KEY", "shhhh"),
        # DEBUG_TB_INTERCEPT_REDIRECTS=True,
    )
    app.config.update(config)

    DebugToolbarExtension(app)

    connect_db(app)
    bcrypt.init_app(app)

    app.register_blueprint(routes_auth.bp)
    app.register_blueprint(routes_cafes.bp)
    app.register_blueprint(routes_home.bp)
    app.register_blueprint(routes_users.bp)
    app.register_blueprint(routes_likes_api.bp)

    return app
