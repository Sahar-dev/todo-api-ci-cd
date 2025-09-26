import pytest
from app.models import Todo
from datetime import datetime

class TestTodoModel:
    def test_todo_creation(self):
        todo = Todo(title="Test Todo", description="Test Description")
        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.completed == False
        assert isinstance(todo.created_at, datetime)
    
    def test_todo_to_dict(self):
        todo = Todo(title="Test Todo", description="Test Description")
        todo_dict = todo.to_dict()
        
        assert todo_dict['title'] == "Test Todo"
        assert todo_dict['description'] == "Test Description"
        assert todo_dict['completed'] == False
        assert 'id' in todo_dict
        assert 'created_at' in todo_dict