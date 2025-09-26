import pytest
from app import create_app, db
from app.models import Todo

class TestTodoRoutes:
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
    def client(self, app):
        return app.test_client()
    
    @pytest.fixture
    def sample_todo(self, app):
        with app.app_context():
            todo = Todo(title="Test Todo")
            db.session.add(todo)
            db.session.commit()
            return todo
    
    def test_get_todos(self, client, sample_todo):
        response = client.get('/api/todos')
        assert response.status_code == 200
        assert len(response.json) == 1
    
    def test_create_todo(self, client):
        data = {
            'title': 'New Todo',
            'description': 'New Description'
        }
        response = client.post('/api/todos', json=data)
        assert response.status_code == 201
        assert response.json['title'] == 'New Todo'