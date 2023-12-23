from flask import Blueprint, session, g, flash, render_template, redirect

from config import CURR_USER_KEY
from models import db, User
from forms import UserSignupForm, UserLoginForm
from sqlalchemy.exc import IntegrityError

bp = Blueprint("auth", __name__)

#######################################
# auth & auth routes


@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@bp.route("/signup", methods=["GET", "POST"])
def signup():
    """ Handle new user signup.

    Create a new user and add to Database. Redirect to cafe list.

    If form not valid, re-present form.

    If a user exists with intended username: flash a message and re-present form.
    """

    do_logout()

    form = UserSignupForm()

    if form.validate_on_submit():
        user = User.register(
            username=form.username.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            description=form.description.data,
            password=form.password.data,
            email=form.email.data,
            image_url=form.image_url.data or None
        )

        try:
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", "danger")
            return render_template("auth/signup-form.html", form=form)

        do_login(user)

        flash(f"Signup successful! You are logged in as {user.username}")
        return redirect("/cafes")


@bp.route("/login", methods=["GET", "POST"])
def login():
    """ Handle user login. Redirects to cafe list on success"""

    form = UserLoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data, form.password.data)

        if user:
            do_login(user)
            flash(f"{user.username} logged in!", "success")
            return redirect("/cafes")

        flash("Invalid username or password", "danger")

    return render_template("/auth/login-form.html", form=form)

@bp.post("/logout")
def logout():
    """ Handle user log out. Redirect to homepage"""

    do_logout()

    flash("You have successfully logged out.", "success")
    return redirect("/")