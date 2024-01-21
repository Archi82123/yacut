from datetime import datetime
import string

from flask import url_for

from yacut import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(128), nullable=False)
    short = db.Column(db.String(16), unique=True, nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self) -> dict:
        return dict(
            url=self.original,
            short_link=url_for(
                'redirect_view',
                short_id=self.short,
                _external=True
            )
        )

    def from_dict(self, data: dict) -> None:
        if 'url' in data:
            setattr(self, 'original', data['url'])
        if 'custom_id' in data:
            setattr(self, 'short', data['custom_id'])

    def valid_short_check(short_id: str) -> bool:
        if len(short_id) > 16:
            return False
        for char in short_id:
            if char not in string.ascii_letters and char not in string.digits:
                return False
        return True
