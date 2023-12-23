from flask import Blueprint, render_template

bp = Blueprint("home", __name__)

# homepage

@bp.get("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")
