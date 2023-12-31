"""Data models for Flask Cafe"""


from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()


class City(db.Model):
    """Cities for cafes."""

    __tablename__ = "cities"

    code = db.Column(
        db.Text,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    state = db.Column(
        db.String(2),
        nullable=False,
    )

    @classmethod
    def city_choices(cls):
        """Return [(city.code, city.name), ...] to use as choices in form"""

        cities = cls.query.order_by("name").all()
        return [(city.code, city.name) for city in cities]


class Cafe(db.Model):
    """Cafe information."""

    __tablename__ = "cafes"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    url = db.Column(
        db.Text,
        nullable=False,
    )

    address = db.Column(
        db.Text,
        nullable=False,
    )

    city_code = db.Column(
        db.Text,
        db.ForeignKey("cities.code"),
        nullable=False,
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-cafe.jpg",
    )

    city = db.relationship("City", backref="cafes")

    liking_users = db.relationship(
        'User',
        secondary='likes',
        backref='liked_cafes'
    )

    def __repr__(self):
        return f"<Cafe id={self.id} name='{self.name}'>"

    def get_city_state(self):
        """Return "city, state" for cafe."""

        city = self.city
        return f"{city.name}, {city.state}"


class User(db.Model):
    """A user of the site"""

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True
    )

    admin = db.Column(
        db.Boolean,
        nullable=False,
        default=False
    )

    email = db.Column(
        db.Text,
        nullable=False
    )

    first_name = db.Column(
        db.Text,
        nullable=False
    )

    last_name = db.Column(
        db.Text,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.Text,
        nullable=False,
        default="/static/images/default-pic.png"
    )

    hashed_password = db.Column(
        db.Text,
        nullable=False
    )

    def __repr__(self):
        return f"<User id = {self.id}, username = '{self.username}'>"

    def get_full_name(self):
        """Return full name of user"""

        return f"{self.first_name} {self.last_name}"

    @classmethod
    def register(cls,
                 username,
                 email,
                 first_name,
                 last_name,
                 description,
                 password,
                 admin=False,
                 image_url=None):
        """Register user on the site

        Hashes the password and adds user to database
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode("utf8")

        user = cls(
            username=username,
            admin=admin,
            email=email,
            first_name=first_name,
            last_name=last_name,
            description=description,
            hashed_password=hashed_pwd,
            image_url=image_url
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with 'username' and 'password'"""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.hashed_password, password):
            return user

        else:
            return False


class Like(db.Model):
    """A user can like a cafe."""

    __tablename__ = "likes"

    def __repr__(self):
        return f"<Like user_id={self.user_id} cafe_id={self.cafe_id}>"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True,
    )

    cafe_id = db.Column(
        db.Integer,
        db.ForeignKey('cafes.id'),
        primary_key=True,
    )

    user = db.relationship('User', backref='likes')
    cafe = db.relationship('Cafe', backref='cafes')


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)
