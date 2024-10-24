from sqlalchemy.orm import Session
from database import SessionLocal

def get_db() -> Session:
    db = SessionLocal()  # 新しいセッションを開始
    try:
        yield db  # セッションを返す
    finally:
        db.close()  # セッションを閉じる
