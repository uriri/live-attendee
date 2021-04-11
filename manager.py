from flask_script import Manager
from ms_teams_live import create_app

from ms_teams_live.scripts.db import InitDB

if __name__ == "__main__":
    manager = Manager(create_app)
    manager.add_command("init_db", InitDB)
    manager.run()
