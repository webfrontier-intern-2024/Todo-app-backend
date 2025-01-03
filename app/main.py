from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy import Date
from .database import get_db
from .models import Todo, Tag
from .schemas import TodoUpdate
from datetime import date
from fastapi.responses import RedirectResponse

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    todos = db.query(Todo).all()
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add/")
def add_todo(
    title: str = Form(...),
    description: str = Form(None),
    datetime: date = Form(...),  
    tags: str = Form(None),  
    db: Session = Depends(get_db)  
):
    tags_list = tags.split(",") if tags else []  

    try:
        new_todo = Todo(title=title, description=description, datetime=datetime)
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
        db.rollback()  
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

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Todoの属性を更新
    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.datetime = todo_update.datetime

    # タグの更新処理
    todo.tags.clear()  # 既存のタグをクリア
    tags_list = todo_update.tags.split(",") if todo_update.tags else []  # 新しいタグリストを取得
    for tag_name in tags_list:
        tag_name = tag_name.strip()
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
            db.commit()  
            db.refresh(tag)
        todo.tags.append(tag)
    db.commit()
    db.refresh(todo)  
    return todo

@app.post("/toggle_complete/{todo_id}")
async def toggle_complete(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo item not found")
    
    todo.completed = not todo.completed  # 完了状態の切り替え
    db.commit()
    
    return RedirectResponse(url="/", status_code=303)   