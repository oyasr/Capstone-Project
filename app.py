from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


if __name__ == "__main__":
    app.run(debug=True)
