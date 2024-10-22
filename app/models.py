from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

todo_tag = Table(
    'todo_tag', Base.metadata,
    Column('todo_id', Integer, ForeignKey('todos.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)

class Todo(Base):
    __tablename__ = 'todos'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    tags = relationship('Tag', secondary=todo_tag, back_populates='todos')

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    todos = relationship('Todo', secondary=todo_tag, back_populates='tags')
