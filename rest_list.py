from fastapi import FastAPI, HTTPException, Query, Path
from pydantic import BaseModel
import sqlite3


############ http://127.0.0.1:8000/ , use /docs ############

app = FastAPI(title="Message API")
DB_NAME = "messages.db"

# Pydantic model for POST requests
class Message(BaseModel):
    text: str

# Initialize the DB and create table if it doesn't exist
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL
            )
        """)
init_db()



# GET all messages
@app.get("/messages", response_model=list[dict])
def get_messages():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        return [{"id": row[0], "text": row[1]} for row in rows]


# GET message by ID
@app.get("/messages/{id}", response_model=dict)
def get_message(id: int = Path(...)):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages WHERE id = ?", (id,))
        row = cursor.fetchone()
        if row:
            return {"id": row[0], "text": row[1]}
        else:
            raise HTTPException(status_code=404, detail="Message not found")

# POST new message
@app.post("/messages", response_model=dict)
def create_message(message: Message):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO messages (text) VALUES (?)", (message.text,))
        conn.commit()
        return {"id": cursor.lastrowid, "text": message.text}


# GET endpoint to retrieve all messages
@app.get("/messages/", response_model=list[dict])
def get_messages():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, text FROM messages")
        rows = cursor.fetchall()
        return [{"id": row[0], "text": row[1]} for row in rows]

# PUT message by ID (replace or insert)
@app.put("/messages/{id}", response_model=dict)
def put_message(id: int, message: Message):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET text = ? WHERE id = ?", (message.text, id))
        if cursor.rowcount == 0:
            cursor.execute("INSERT INTO messages (id, text) VALUES (?, ?)", (id, message.text))
        conn.commit()
        return {"id": id, "text": message.text}

@app.patch("/messages/{id}", response_model=dict)
def patch_message(id: int, message: Message):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("UPDATE messages SET text = ? WHERE id = ?", (message.text, id))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        conn.commit()
        return {"id": id, "text": message.text}

# DELETE message by ID
@app.delete("/messages/{id}", response_model=dict)
def delete_message(id: int):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM messages WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Message not found")
        conn.commit()
        return {"detail": f"Message with id {id} deleted"}

# Optional: Home route
@app.get("/")
def home():
    return {"message": "Welcome to the Message API. Use /docs to try it out."}


