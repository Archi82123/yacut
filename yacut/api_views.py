from flask import jsonify, request

from yacut import app, db
from yacut.models import URLMap
from yacut.views import get_unique_short_id
from yacut.error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST'])
def url_create() -> jsonify:
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
    db.session.add(url)
    db.session.commit()
    return jsonify(url.to_dict()), 201


@app.route('/api/id/<short_id>/', methods=['GET'])
def get_original_url(short_id) -> jsonify:
    url = URLMap().query.filter_by(short=short_id).first()
    if not url:
        raise InvalidAPIUsage('Указанный id не найден', 404)
    original_url = url.original
    return jsonify({'url': original_url}), 200
