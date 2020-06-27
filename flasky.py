import os
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)

if __name__ == "__main__":
    manager.run()
