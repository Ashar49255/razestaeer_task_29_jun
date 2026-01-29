from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# Allow frontend to call API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database settings - CHANGE THESE
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "your_password"  # Change this
DB_NAME = "userdb"

# User model
class User(BaseModel):
    username: str
    designation: str

# Connect to database
def get_db():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

# Create table on startup
@app.on_event("startup")
def create_table():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255),
            designation VARCHAR(255)
        )
    """)
    db.commit()
    cursor.close()
    db.close()

# Test endpoint
@app.get("/")
def home():
    return {"message": "API is working"}

# Save user
@app.post("/users")
def add_user(user: User):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO users (username, designation) VALUES (%s, %s)",
        (user.username, user.designation)
    )
    db.commit()
    user_id = cursor.lastrowid
    cursor.close()
    db.close()
    return {"id": user_id, "username": user.username, "designation": user.designation}

# Get all users
@app.get("/users")
def get_users():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users ORDER BY id DESC")
    users = cursor.fetchall()
    cursor.close()
    db.close()
    return users

# Run with: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
