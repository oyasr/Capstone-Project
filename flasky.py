import os
from app import create_app, db
from flask_script import Manager
from app.models import Category, Product
from flask_migrate import Migrate, MigrateCommand

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db)
manager = Manager(app)


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Category=Category, Product=Product)


@manager.command
def test(test_names):
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


manager.add_command('db', MigrateCommand)


if __name__ == "__main__":
    manager.run()
