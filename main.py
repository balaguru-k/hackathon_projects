from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Email
from datetime import datetime
import os

from database import get_emails
from triage import triage_email

from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse

from reply import generate_reply

from fastapi.staticfiles import StaticFiles



# Single FastAPI app
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# ----------------------------
# Health check
@app.get("/")
def root():
    return {"message": "Hackathon Email Assistant is running"}

# ----------------------------
# Show dummy emails (from database.py)
@app.get("/emails/dummy")
def list_dummy_emails():
    return get_emails()

# ----------------------------
# Triage dummy emails
@app.get("/triage")
def triage():
    emails = get_emails()
    return [triage_email(e) for e in emails]

# ----------------------------
# Actual DB setup
DB_URL = os.getenv("DATABASE_URL", "sqlite:///./emails.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

# ----------------------------
# Show real emails from DB
@app.get("/emails")
def list_emails():
    db = SessionLocal()
    emails = db.query(Email).order_by(Email.priority.desc().nullslast()).all()
    out = [
        {
            "id": e.id,
            "sender": e.sender,
            "subject": e.subject,
            "priority": e.priority or "not_urgent",
            "sentiment": e.sentiment or "neutral",
            "status": e.status,
        }
        for e in emails
    ]
    db.close()
    return out



# ... keep your existing imports and setup ...

# ----------------------------
# Filter emails by priority or sentiment
@app.get("/emails/filter")
def filter_emails(priority: str = Query(None), sentiment: str = Query(None)):
    db = SessionLocal()
    query = db.query(Email)
    if priority:
        query = query.filter(Email.priority == priority)
    if sentiment:
        query = query.filter(Email.sentiment == sentiment)
    emails = query.all()
    out = [
        {
            "id": e.id,
            "sender": e.sender,
            "subject": e.subject,
            "priority": e.priority or "not_urgent",
            "sentiment": e.sentiment or "neutral",
            "status": e.status,
        }
        for e in emails
    ]
    db.close()
    return out

# ----------------------------
# Mark an email as resolved
@app.post("/emails/{email_id}/resolve")
def resolve_email(email_id: int):
    db = SessionLocal()
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        db.close()
        return JSONResponse(status_code=404, content={"error": "Email not found"})
    
    email.status = "resolved"
    db.commit()
    db.refresh(email)
    db.close()
    return {"message": "Email resolved", "id": email.id, "status": email.status}



@app.get("/emails/{email_id}/suggest-reply")
def suggest_reply(email_id: int):
    db = SessionLocal()
    email = db.query(Email).filter(Email.id == email_id).first()
    if not email:
        db.close()
        return JSONResponse(status_code=404, content={"error": "Email not found"})
    
    reply = generate_reply(email)
    db.close()
    return {"email_id": email.id, "suggested_reply": reply}


