from http import HTTPStatus

from flask import jsonify, request

from yacut import app
from yacut.error_handlers import InvalidAPIUsage
from yacut.models import URLMap
from yacut.views import get_unique_short_id


@app.route('/api/id/', methods=('POST',))
def url_create() -> tuple:
    data = request.get_json()
    if not data:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    if 'url' not in data:
        raise InvalidAPIUsage('\"url\" является обязательным полем!')
    custom_id = data.get('custom_id')
    if not custom_id:
        data['custom_id'] = get_unique_short_id()
        custom_id = data.get('custom_id')
    if URLMap.query.filter_by(short=custom_id).first() is not None:
        raise InvalidAPIUsage(
            'Предложенный вариант короткой ссылки уже существует.'
        )
    if not URLMap.valid_short_check(custom_id):
        raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
    url = URLMap()
    url.from_dict(data)
    url.db_save()
    return jsonify(url.to_dict()), HTTPStatus.CREATED


@app.route('/api/id/<short_id>/', methods=('GET',))
def get_original_url(short_id) -> tuple:
    url = URLMap().query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    original_url = url.original
    return jsonify({'url': original_url}), HTTPStatus.OK
