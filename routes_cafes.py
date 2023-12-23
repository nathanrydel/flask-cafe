from flask import Blueprint, render_template, redirect, flash, g, url_for

from forms import CafeAddEditForm
from models import City, Cafe, db

bp = Blueprint("cafes", __name__)

#######################################
# cafes


@bp.get("/cafes")
def cafe_list_all():
    """Return list of all cafes."""

    cafes = Cafe.query.order_by("name").all()

    return render_template(
        "cafe/list.html",
        cafes=cafes,
    )


@bp.get("/cafes/<int:cafe_id>")
def cafe_detail(cafe_id):
    """Show detail for cafe."""

    cafe = Cafe.query.get_or_404(cafe_id)

    return render_template(
        "cafe/detail.html",
        cafe=cafe,
    )

@bp.route("/cafes/add", methods=["GET", "POST"])
def cafe_add():
    """Show add form / handle adding of cafe"""

    # if not g.user:
    #     flash("You must be signed in to add a cafe")
    #     return redirect("/login")

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