from flask import Blueprint, render_template, redirect, session, g
# from werkzeug.exceptions import Unauthorized

# from config import CURR_USER_KEY, NOT_LOGGED_IN_MSG
# from models import db, User

bp = Blueprint("auth", __name__)

#######################################
# auth & auth routes


# @bp.before_request
# def add_user_to_g():
#     """If we're logged in, add curr user to Flask global."""

#     if CURR_USER_KEY in session:
#         g.user = User.query.get(session[CURR_USER_KEY])

#     else:
#         g.user = None


# def do_login(user):
#     """Log in user."""

#     session[CURR_USER_KEY] = user.id


# def do_logout():
#     """Logout user."""

#     if CURR_USER_KEY in session:
#         del session[CURR_USER_KEY]
