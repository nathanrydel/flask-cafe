from flask import Blueprint, render_template, redirect, flash, url_for, g, session

from config import CURR_USER_KEY
from forms import CafeAddEditForm
from models import db, City, Cafe, User

bp = Blueprint("cafes", __name__)

@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

#######################################
# cafes


@bp.get("/cafes")
def cafe_list_all():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by("name").all()

    return render_template(
        "cafe/list.html",
        cafes=cafes,
        can_add=g.user and g.user.admin
    )


@bp.get("/cafes/<int:cafe_id>")
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    if g.user:
        liked = g.user in cafe.liking_users
    else:
        liked = None

    return render_template(
        "cafe/detail.html",
        cafe=cafe,
        show_edit=g.user and g.user.admin,
        liked=liked
    )

@bp.route("/cafes/add", methods=["GET", "POST"])
def cafe_add():
    """Show add form / handle adding of cafe"""

    if not g.user or not g.user.admin:
        flash("Only admins can add cafes.", "danger")
        return redirect("/login")

    form = CafeAddEditForm()
    form.city_code.choices = City.city_choices()

    if form.validate_on_submit():
        cafe = Cafe(
            name=form.name.data,
            description=form.description.data,
            url=form.url.data,
            address=form.address.data,
            city_code=form.city_code.data,
            image_url=form.image_url.data or None,
        )

        db.session.add(cafe)
        db.session.commit()

        flash(f"{cafe.name} added.", "success")
        return redirect(url_for("cafes.cafe_detail", cafe_id=cafe.id))

    else:
        return render_template("/cafe/add-form.html", form=form)


@bp.route("/cafes/<int:cafe_id>/edit", methods=["GET", "POST"])
def cafe_edit(cafe_id):
    """Show edit form / handle editing of cafe"""

    if not g.user or not g.user.admin:
        flash("Only admins can edit cafes.", "danger")
        return redirect("/login")

    cafe = Cafe.query.get_or_404(cafe_id)

    form = CafeAddEditForm(obj=cafe)
    form.city_code.choices = City.city_choices()

    if form.validate_on_submit():
        cafe.name = form.name.data
        cafe.description = form.description.data
        cafe.url = form.url.data
        cafe.address = form.address.data
        cafe.city_code = form.city_code.data
        cafe.image_url = form.image_url.data

        db.session.commit()

        flash(f"{cafe.name} edited.", "success")
        return redirect(url_for("cafes.cafe_detail", cafe_id=cafe.id))

    else:
        return render_template("cafe/edit-form.html", cafe=cafe, form=form)