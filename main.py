from fastapi import FastAPI, HTTPException, Query
from models import Todo
from database import get_db_connection, init_db
from typing import Optional

app = FastAPI()
init_db()

@app.get("/")
def root():
    return {"message": "✅ FastAPI Todo App with SQLite"}

@app.get("/todos")
def get_todos(completed: Optional[bool] = Query(None)):
    conn = get_db_connection()
    cursor = conn.cursor()

    if completed is not None:
        cursor.execute("SELECT * FROM todos WHERE completed = ?", (int(completed),))
    else:
        cursor.execute("SELECT * FROM todos")

    todos = cursor.fetchall()
    conn.close()
    return [
    {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
        "due_date": row["due_date"],
        "tags": row["tags"]
    } for row in todos
]

@app.post("/todos")
def create_todo(todo: Todo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO todos (title, completed, due_date, tags) VALUES (?, ?, ?, ?)",
        (todo.title, int(todo.completed), todo.due_date, todo.tags)
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return {"id": new_id, **todo.dict()}

@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: Todo):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE todos SET title = ?, completed = ?, due_date = ?, tags = ? WHERE id = ?",
        (todo.title, int(todo.completed), todo.due_date, todo.tags, todo_id)
    )
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return {"message": "Updated successfully", "todo": todo}

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return {"message": "Deleted successfully"}
