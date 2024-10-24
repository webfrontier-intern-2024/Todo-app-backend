from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from database import Base  # ここで Base をインポートする

# データベース接続情報
DATABASE_URL = "postgresql://codeserver:rH8,KeGa@localhost/todo_db"

# エンジンの作成
engine = create_engine(DATABASE_URL)

# セッションの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# データベースセッションを取得する関数
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    

    # 'todos' リレーションを設定
    todos = relationship("todo_tags", back_populates="tag")

class TodoTag(Base):
    __tablename__ = "todo_tags"
    todo_id = Column(Integer, ForeignKey("todos.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id"), primary_key=True)

    # 'tag' リレーションを設定
    tag = relationship("Tag", back_populates="todos")

