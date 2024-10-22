from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 正しいデータベース接続情報を指定
DATABASE_URL = "postgresql://codeserver:Tt1225912@localhost/todo_db"

# エンジンの作成
engine = create_engine(DATABASE_URL)

# セッションローカルの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ベースクラスの作成
Base = declarative_base()
