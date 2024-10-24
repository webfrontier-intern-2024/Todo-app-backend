from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base

# 中間テーブルの定義
todo_tag = Table(
    'todo_tag', Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class Todo(Base):
    __tablename__ = 'todos'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    # リレーションシップの定義
    tags = relationship('Tag', secondary=todo_tag, back_populates='todos')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    # リレーションシップの定義
    todos = relationship('Todo', secondary=todo_tag, back_populates='tags')
