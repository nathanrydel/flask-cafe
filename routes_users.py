from flask import Blueprint, render_template, redirect, flash, g, session

from config import CURR_USER_KEY, NOT_LOGGED_IN_MSG
from forms import UserEditForm
from models import db, User

bp = Blueprint("users", __name__)

@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@bp.get("/profile")
def user_profile():
    """Show profile for user."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    return render_template("profile/detail.html", user=g.user)


@bp.route('/profile/edit', methods=["GET", "POST"])
def profile_edit():
    """Edit profile for user."""

    if not g.user:
        flash(NOT_LOGGED_IN_MSG, "danger")
        return redirect("/login")

    user = g.user

    form = UserEditForm(obj=g.user)

    if form.validate_on_submit():
        user.first_name = form.first_name.data
        user.last_name = form.last_name.data
        user.description = form.description.data
        user.email = form.email.data
        user.description = form.description.data
        user.image_url = form.image_url.data
        db.session.commit()

        flash("Profile edited.", "success")
        return redirect("/profile")

    else:
        return render_template('profile/edit-form.html', form=form)