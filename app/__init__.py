from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.exceptions import NotFound, BadRequest

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    # Import models here
    from app.models.book import Book

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import books_bp
    app.register_blueprint(books_bp)

    # we can register an error handler to process errors raised by the 
    # application, such as a 404 from get_or_404. for more details about
    # error handlers, refer to
    # https://flask.palletsprojects.com/en/2.0.x/errorhandling/#error-handlers 
    @app.errorhandler(NotFound)
    @app.errorhandler(BadRequest)
    def handle_invalid_usage(error):
        return jsonify(error.description), error.code

    return app
