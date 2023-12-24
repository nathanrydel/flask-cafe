from flask import Blueprint, g, session, render_template
from models import User
from config import CURR_USER_KEY

bp = Blueprint("home", __name__)


@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


# homepage

@bp.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")
