import random

from flask import Response, flash, redirect, render_template

from yacut import app
from yacut.forms import URLMapForm
from yacut.models import URLMap
from yacut.settings import ALL_CHARS


def get_unique_short_id() -> str:
    while True:
        random_chars = random.choices(ALL_CHARS, k=6)
        short_id = ''.join(random_chars)
        if not URLMap.query.filter_by(short=short_id).first():
            return short_id


@app.route('/', methods=('GET', 'POST'))
def index_view() -> Response:
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = get_unique_short_id()
    if URLMap.query.filter_by(short=custom_id).first():
        flash(
            'Предложенный вариант короткой ссылки уже существует.',
            'uniq-error-message'
        )
        return render_template('index.html', form=form)
    url = URLMap(
        original=form.original_link.data,
        short=custom_id,
    )
    flash({'original': url.original, 'short': url.short}, 'success')
    url.db_save()
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=('GET',))
def redirect_view(short_id: str) -> Response:
    url = URLMap().query.filter_by(short=short_id).first_or_404()
    return redirect(url.original)
