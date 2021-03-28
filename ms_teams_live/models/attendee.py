from datetime import datetime

from ms_teams_live import db


class Attendee(db.Model):
    __tablename__ = "attendees"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    event_title = db.Column(db.String(100))
    name = db.Column(db.String(50))
    is_presenter = db.Column(db.Boolean)
    join_timestamp = db.Column(db.DateTime)
    left_timestamp = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __init__(
        self,
        event_title=None,
        name=None,
        is_presenter=None,
        join_timestamp=None,
        left_timestamp=None,
    ):
        self.event_title = event_title
        self.name = name
        self.is_presenter = is_presenter
        self.join_timestamp = join_timestamp
        self.left_timestamp = left_timestamp
