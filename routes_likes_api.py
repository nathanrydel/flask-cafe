from flask import Blueprint, g, session, request, jsonify

from config import CURR_USER_KEY
from models import db, Cafe, User, Like

bp = Blueprint("likes_api", __name__)

@bp.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

@bp.get("/api/likes")
def likes_cafe():
    """Does user like a cafe?"""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.args['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    like = Like.query.filter_by(user_id=g.user.id, cafe_id=cafe.id).first()
    likes = like is not None

    return jsonify({"likes": likes})


@bp.post("/api/like")
def like_cafe():
    """Like a cafe."""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.json['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    g.user.liked_cafes.append(cafe)
    db.session.commit()

    res = {"liked": cafe.id}
    return jsonify(res)


@bp.post("/api/unlike")
def unlike_cafe():
    """Unlike a cafe."""

    if not g.user:
        return jsonify({"error": "Not logged in"})

    cafe_id = int(request.json['cafe_id'])
    cafe = Cafe.query.get_or_404(cafe_id)

    Like.query.filter_by(cafe_id=cafe_id, user_id=g.user.id).delete()
    db.session.commit()

    res = {"unliked": cafe.id}
    return jsonify(res)