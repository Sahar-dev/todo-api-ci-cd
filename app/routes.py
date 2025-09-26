from flask import Blueprint, request, jsonify
from app.models import Todo
from app import db

main = Blueprint('main', __name__)

@main.route('/api/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])

@main.route('/api/todos', methods=['POST'])
def create_todo():
    data = request.get_json()
    todo = Todo(
        title=data.get('title'),
        description=data.get('description', '')
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify(todo.to_dict()), 201

@main.route('/api/todos/<int:todo_id>', methods=['GET'])
def get_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    return jsonify(todo.to_dict())

@main.route('/api/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    data = request.get_json()
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify(todo.to_dict())

@main.route('/api/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todo = Todo.query.get_or_404(todo_id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204

@main.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})