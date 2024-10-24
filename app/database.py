from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# データベース接続情報
DATABASE_URL = "postgresql://codeserver:rH8,KeGa@localhost/todo_db"

# PostgreSQL用のエンジンを作成
engine = create_engine(DATABASE_URL)  # connect_argsのオプションを削除
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db  # セッションをリクエストで使用
    finally:
        db.close()
