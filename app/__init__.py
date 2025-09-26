from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///todo.db",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    # Import models so they register with SQLAlchemy
    from . import models

    # Import routes so they register with the app
    from .routes import main as main_bp
    app.register_blueprint(main_bp)

    # Register CLI command
    @app.cli.command("init-db")
    def init_db_command():
        """Initialize the database with sample data"""
        with app.app_context():
            db.create_all()
            from .models import Todo
            if Todo.query.count() == 0:
                sample_todos = [
                    Todo(title="Learn CI/CD",
                         description="Build a portfolio project"),
                    Todo(title="Write tests", description="Unit and API tests"),
                    Todo(title="Deploy application",
                         description="Set up pipeline"),
                ]
                db.session.add_all(sample_todos)
                db.session.commit()
            print("Initialized the database.")

    return app
