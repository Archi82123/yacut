from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField
from wtforms.validators import URL, DataRequired, Length, Optional

from settings import MAX_CUSTOM_ID_LENGTH, MAX_ORIGINAL_LINK_LENGTH, MIN_LENGTH


class URLMapForm(FlaskForm):
    original_link = URLField(
        'Длинная ссылка',
        validators=(DataRequired(message='Обязательное поле'),
                    URL(message='Введите корректный URL адрес'),
                    Length(MIN_LENGTH, MAX_ORIGINAL_LINK_LENGTH))
    )
    custom_id = StringField(
        'Ваш вариант короткой ссылки',
        validators=(Length(MIN_LENGTH, MAX_CUSTOM_ID_LENGTH),
                    Optional())
    )
    submit = SubmitField('Создать')
