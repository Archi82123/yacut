from datetime import datetime

from flask import url_for

from yacut import db
from yacut.settings import (ALL_CHARS, MAX_CUSTOM_ID_LENGTH,
                            MAX_ORIGINAL_LINK_LENGTH)


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(MAX_ORIGINAL_LINK_LENGTH), nullable=False)
    short = db.Column(
        db.String(MAX_CUSTOM_ID_LENGTH),
        unique=True,
        nullable=False
    )
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
            if char not in ALL_CHARS:
                return False
        return True

    def db_save(self):
        db.session.add(self)
        db.session.commit()
