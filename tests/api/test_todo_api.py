import pytest
import requests
import time


class TestTodoAPI:
    BASE_URL = "http://localhost:5000/api"

    # ---------------- Fixtures ---------------- #
    @pytest.fixture(autouse=True, scope="function")
    def wait_for_app(self):
        """Wait for the application to start before tests run"""
        max_retries = 10
        for i in range(max_retries):
            try:
                response = requests.get("http://localhost:5000/health", timeout=5)
                if response.status_code == 200:
                    break
            except requests.exceptions.RequestException:
                if i < max_retries - 1:
                    time.sleep(2)
                else:
                    pytest.fail("❌ Application failed to start")

    @pytest.fixture(autouse=True, scope="function")
    def clean_db(self):
        """Ensure database is clean before each test"""
        todos = requests.get(f"{self.BASE_URL}/todos").json()
        for todo in todos:
            requests.delete(f"{self.BASE_URL}/todos/{todo['id']}")

    # ---------------- Positive Tests ---------------- #
    def test_health_endpoint(self):
        response = requests.get("http://localhost:5000/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

    def test_get_all_todos(self):
        response = requests.get(f"{self.BASE_URL}/todos")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_create_todo(self):
        data = {"title": "API Test Todo", "description": "Created via API test"}
        response = requests.post(f"{self.BASE_URL}/todos", json=data)
        assert response.status_code == 201
        todo = response.json()
        assert todo["title"] == "API Test Todo"
        assert set(todo.keys()) == {"id", "title", "description", "completed", "created_at"}

    def test_get_single_todo(self):
        data = {"title": "Test Todo"}
        create_response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = create_response.json()["id"]

        response = requests.get(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 200
        assert response.json()["id"] == todo_id

    def test_update_todo(self):
        data = {"title": "Original Title"}
        create_response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = create_response.json()["id"]

        update_data = {"title": "Updated Title", "completed": True}
        response = requests.put(f"{self.BASE_URL}/todos/{todo_id}", json=update_data)
        assert response.status_code == 200
        updated = response.json()
        assert updated["title"] == "Updated Title"
        assert updated["completed"] is True

    def test_delete_todo(self):
        data = {"title": "Todo to delete"}
        create_response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = create_response.json()["id"]

        response = requests.delete(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 204

        response = requests.get(f"{self.BASE_URL}/todos/{todo_id}")
        assert response.status_code == 404

    # ---------------- Negative / Edge Tests ---------------- #
    def test_get_nonexistent_todo(self):
        response = requests.get(f"{self.BASE_URL}/todos/999999")
        assert response.status_code == 404

    def test_delete_nonexistent_todo(self):
        response = requests.delete(f"{self.BASE_URL}/todos/999999")
        assert response.status_code == 404

    def test_update_with_invalid_data(self):
        data = {"title": "Valid Todo"}
        create_response = requests.post(f"{self.BASE_URL}/todos", json=data)
        todo_id = create_response.json()["id"]

        # Missing title, invalid type for completed
        bad_data = {"title": "", "completed": "not-a-bool"}
        response = requests.put(f"{self.BASE_URL}/todos/{todo_id}", json=bad_data)
        assert response.status_code in (400, 422)  # Depending on how API handles it

    # ---------------- Performance Tests ---------------- #
    def test_response_time(self):
        response = requests.get(f"{self.BASE_URL}/todos")
        assert response.elapsed.total_seconds() < 0.5, "API is too slow!"
