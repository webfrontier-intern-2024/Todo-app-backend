from sqlalchemy.orm import Session
from models import Todo

def create_todo(db: Session, title: str):
    new_todo = Todo(title=title)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

def get_todos(db: Session):
    return db.query(Todo).all()

def delete_todo(db: Session, todo_id: int):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
