from flask import Blueprint, render_template, redirect, flash, url_for, g, session

from config import CURR_USER_KEY
from forms import CafeAddEditForm
from models import db, City, Cafe, User

bp = Blueprint("likes_api", __name__)

@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None