from flask_script import Command
from ms_teams_live import db


class InitDB(Command):
    "create database"

    def run(self):
        db.create_all()
