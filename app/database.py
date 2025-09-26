from app import db
from app.models import Todo

def init_db():
    db.create_all()
    # Add some sample data
    if Todo.query.count() == 0:
        sample_todos = [
            Todo(title="Learn CI/CD", description="Build a portfolio project"),
            Todo(title="Write tests", description="Unit and API tests"),
            Todo(title="Deploy application", description="Set up pipeline")
        ]
        db.session.add_all(sample_todos)
        db.session.commit()