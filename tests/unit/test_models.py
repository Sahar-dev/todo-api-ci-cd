import pytest
from app import create_app, db
from app.models import Todo
from datetime import datetime


class TestTodoModel:
    @pytest.fixture
    def app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        with app.app_context():
            db.create_all()
            yield app
            db.drop_all()

    @pytest.fixture
    def session(self, app):
        with app.app_context():
            yield db.session

    def test_todo_creation(self, session):
        todo = Todo(title="Test Todo", description="Test Description")
        session.add(todo)
        session.commit()

        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.completed is False
        assert isinstance(todo.created_at, datetime)

    def test_todo_to_dict(self, session):
        todo = Todo(title="Test Todo", description="Test Description")
        session.add(todo)
        session.commit()

        todo_dict = todo.to_dict()

        assert todo_dict['title'] == "Test Todo"
        assert todo_dict['description'] == "Test Description"
        assert todo_dict['completed'] is False
        assert 'id' in todo_dict
        assert 'created_at' in todo_dict
