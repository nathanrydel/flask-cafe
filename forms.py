"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Length, Email


class CafeAddEditForm(FlaskForm):
    """Form for adding/editing a cafe"""

    name = StringField(
        "Name",
        validators=[InputRequired()]
    )

    description = TextAreaField(
        "Description",
        validators=[Optional()]
    )

    url = URLField(
        "URL",
        validators=[Optional()]
    )

    address = StringField(
        "Address",
        validators=[InputRequired()]
    )

    city_code = SelectField(
        "City",
        validators=[InputRequired()]
    )

    image_url = URLField(
        "Image",
        validators=[Optional()]
    )


class UserSignupForm(FlaskForm):
    """Form for creating a user on signup"""

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=5, max=20)]
    )

    password = PasswordField(
        "Password",
        validators=[InputRequired(), Length(min=6)]
    )

    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(min=2)]
    )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(min=2)]
    )

    description = TextAreaField(
        "Description",
        validators=[InputRequired()]
    )

    image_url = URLField(
        "Image URL (Optional)",
        validators=[Optional()]
    )
