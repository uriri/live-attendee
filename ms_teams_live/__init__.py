from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config.from_object("ms_teams_live.config.DevelopmentConfig")
    db.init_app(app)

    from ms_teams_live.views.attendee import attendee

    app.register_blueprint(attendee)

    return app
