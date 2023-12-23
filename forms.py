"""Forms for Flask Cafe."""

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SelectField, PasswordField
from wtforms.validators import InputRequired, Optional, Email


class AddCafeForm(FlaskForm):
    """Form for adding a cafe"""

    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[Optional()])
    url = URLField("URL", validators=[Optional()])
    address = StringField("Address", validators=[InputRequired()])
    city = SelectField("City", validators=[InputRequired()])
    image_url = URLField("Image", validators=[Optional()])
