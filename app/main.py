from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from .database import get_db
from .models import Todo, Tag

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
    tags: str = Form(None),  
    db: Session = Depends(get_db)  
):
    tags_list = tags.split(",") if tags else []  

    try:
        new_todo = Todo(title=title, description=description)
        db.add(new_todo)
        db.commit()
        db.refresh(new_todo)

        # タグの処理
        for tag_name in tags_list:
            tag_name = tag_name.strip()
            tag = db.query(Tag).filter(Tag.name == tag_name).first()
            if not tag:
                tag = Tag(name=tag_name)
                db.add(tag)
                db.commit()  
                db.refresh(tag)  
            
            new_todo.tags.append(tag)

        db.commit()  

    except Exception as e:
        db.rollback()  # エラーが発生した場合はロールバック
        raise HTTPException(status_code=500, detail=str(e))  

    return {"message": "リストが追加されました"}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo_item = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo_item:
        raise HTTPException(status_code=404, detail="Todo item not found")

    db.delete(todo_item)
    db.commit()

    return {"message": "タスクが削除されました"}

