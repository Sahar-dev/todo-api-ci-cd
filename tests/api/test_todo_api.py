import pytest
import requests
import time

class TestTodoAPI:
    BASE_URL = "http://localhost:5000/api"
    
    @pytest.fixture
    def setup(self):
        # Wait for app to start
        time.sleep(2)
        
        # Clean up before test
        response = requests.get(f"{self.BASE_URL}/todos")
        if response.status_code == 200:
            todos = response.json()
            for todo in todos:
                requests.delete(f"{self.BASE_URL}/todos/{todo['id']}")
    
    def test_health_check(self):
        response = requests.get("http://localhost:5000/health")
        assert response.status_code == 200
        assert response.json()['status'] == 'healthy'
    
    def test_create_and_get_todo(self, setup):
        # Create todo
        data = {
            'title': 'API Test Todo',
            'description': 'Testing API endpoints'
        }
        response = requests.post(f"{self.BASE_URL}/todos", json=data)
        assert response.status_code == 201
        todo_id = response.json()['id']
        
        # Get todo
        response = requests.get(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()['title'] == 'API Test Todo'
    
    def test_update_todo(self, setup):
        # Create todo
        data = {'title': 'Test Todo'}
        response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = response.json()['id']
        
        # Update todo
        update_data = {'title': 'Updated Todo', 'completed': True}
        response = requests.put(f"{self.BASE_URL}/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        assert response.json()['title'] == 'Updated Todo'
        assert response.json()['completed'] == True
    
    def test_delete_todo(self, setup):
        # Create todo
        data = {'title': 'Todo to delete'}
        response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = response.json()['id']
        
        # Delete todo
        response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 204
        
        # Verify deletion
        response = requests.get(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 404