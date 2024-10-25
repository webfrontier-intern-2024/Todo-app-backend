from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

class TodoTag(Base):
    __tablename__ = "todo_tags"
    todo_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)  
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    # リレーションシップの定義
    tags = relationship('Tag', secondary='todo_tags', back_populates='todos')  

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    todos = relationship('Todo', secondary='todo_tags', back_populates='tags')  