from fastapi import FastAPI, HTTPException
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

# POST endpoint to create a new message
@app.post("/messages/", response_model=dict)
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

# Optional: Home route
@app.get("/")
def home():
    return {"message": "Welcome to the Message API. Use /docs to try it out."}


