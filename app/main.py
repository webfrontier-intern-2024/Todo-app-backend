from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import get_db

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    # データベースからタスクを取得
    todos = db.query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add/")
def add_todo(
    title: str = Form(...),
    description: str = Form(None),
    tags: str = Form(None),  # カンマ区切りでタグを入力
    db: Session = Depends(get_db)  # データベースセッションを取得
):
    tags_list = tags.split(",") if tags else []  # カンマ区切りのタグをリストに変換

    try:
        # 新しいTodoをデータベースに追加
        new_todo = Todo(title=title, description=description)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)  # 追加したTodoのIDを取得

        # タグの処理
        for tag_name in tags_list:
            tag_name = tag_name.strip()  # タグ名の前後の空白を削除
            # 既存のタグを確認、なければ新しいタグを作成
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()  # 新しいタグをコミット
                db.refresh(tag)  # タグの情報を更新
            
            # タグをTodoに追加
            new_todo.tags.append(tag) 

        db.commit()  # 最後にTodoをコミット

    except Exception as e:
        db.rollback()  # エラーが発生した場合はロールバック
        raise HTTPException(status_code=500, detail=str(e))  # エラーハンドリング

    return {"message": "リストが追加されました"}
