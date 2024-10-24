from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import psycopg2
import atexit

# データベース接続
def get_connection():
    return psycopg2.connect(
        dbname='todo_db',
        user='codeserver',
        password='rH8,KeGa',
        host='localhost',
        port='5432'
    )

# アプリケーションのインスタンスを作成
app = FastAPI()

# 静的ファイルの提供
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# テンプレートの設定
templates = Jinja2Templates(directory="app/templates")

# 仮のタスクデータ
class Todo:
    def __init__(self, id, title, tags):
        self.id = id
        self.title = title
        self.tags = [Tag(name) for name in tags]

class Tag:
    def __init__(self, name):
        self.name = name

# 初期タスクデータ
todos = [
    Todo(1, "買い物をする", ["家事"]),
    Todo(2, "レポートを書く", ["勉強", "重要"]),
]

@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "todos": todos})

@app.post("/add/")
def add_todo(
    title: str = Form(...),
    description: str = Form(None),
    tags: str = Form(None)  # カンマ区切りでタグを入力
):
    tags_list = tags.split(",") if tags else []  # カンマ区切りのタグをリストに変換
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()

        # タスクをtodosテーブルに追加
        cursor.execute(
            "INSERT INTO todos (title, description) VALUES (%s, %s) RETURNING id",
            (title, description)
        )
        todo_id = cursor.fetchone()[0]  # 追加されたタスクのIDを取得

        # タグの処理
        for tag_name in tags_list:
            cursor.execute("SELECT id FROM tags WHERE name = %s", (tag_name,))
            tag = cursor.fetchone()

            if tag:
                tag_id = tag[0]
            else:
                cursor.execute("INSERT INTO tags (name) VALUES (%s) RETURNING id", (tag_name,))
                tag_id = cursor.fetchone()[0]

            cursor.execute("INSERT INTO todo_tags (todo_id, tag_id) VALUES (%s, %s)", (todo_id, tag_id))

        # コミットしてトランザクションを確定
        connection.commit()

        # データベースからすべてのタスクを再取得してtodosリストを更新
        cursor.execute("SELECT * FROM todos")
        rows = cursor.fetchall()

        todos.clear()  # 既存のリストをクリア

        # タスクごとに関連するタグを取得
        for row in rows:
            todo_id, title, description = row[0], row[1], row[2]

            # タグの取得
            cursor.execute("""
                SELECT tags.name 
                FROM tags
                JOIN todo_tags ON tags.id = todo_tags.tag_id
                WHERE todo_tags.todo_id = %s
            """, (todo_id,))
            tag_rows = cursor.fetchall()
            tag_names = [tag_row[0] for tag_row in tag_rows]  # タグ名をリストに変換
            
            # タスクを更新
            todos.append(Todo(todo_id, title, tag_names))

    except Exception as e:
        if connection:
            connection.rollback()  # エラーが発生した場合はロールバック
        raise HTTPException(status_code=500, detail=str(e))  # エラーハンドリング
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

    return {"message": "リストが追加されました"}
