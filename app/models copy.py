from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

# 中間テーブルの定義
class TodoTag(Base):
    __tablename__ = "todo_tags"
    todo_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

# Todoモデル
class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    deadline = Column(DateTime, nullable=True)  # 期限フィールド

    # Tagとのリレーションシップ
    tags = relationship('Tag', secondary='todo_tags', back_populates='todos')

# Tagモデル
class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    
    # Todoとのリレーションシップ
    todos = relationship('Todo', secondary='todo_tags', back_populates='tags', cascade="all, delete")
