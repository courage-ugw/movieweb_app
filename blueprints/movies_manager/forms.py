from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class UpdateMovieForm(FlaskForm):
    """
    Allow users to update movie detials
    """
    name = StringField('Name', validators=[ Length(min=2, max=20)])
    year = StringField('Year', validators=[ Length(min=2, max=20)])
    actor = StringField('Actors', validators=[ Length(min=2, max=20)])
    genre = StringField('Genre', validators=[DataRequired(), Length(min=2, max=20)])
    director = StringField('Director', validators=[DataRequired(), Length(min=2, max=20)])
    country = StringField('Country', validators=[DataRequired(), Length(min=2, max=20)])
    rating = StringField('Rating', validators=[DataRequired(), Length(min=2, max=20)])
    plot = TextAreaField('Name', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Update')
