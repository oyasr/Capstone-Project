import os
from app import create_app, db
from flask_script import Manager
from app.models import Category, Product
from flask_migrate import Migrate

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Category=Category, Product=Product)


if __name__ == "__main__":
    manager.run()
