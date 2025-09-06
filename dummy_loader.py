# dummy_loader.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Email
import os
from datetime import datetime, timedelta

DB_URL = os.getenv("DATABASE_URL", "sqlite:///./emails.db")
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)
Base.metadata.create_all(bind=engine)

def load_dummy():
    db = SessionLocal()
    samples = [
        Email(sender="alice@example.com", subject="Support: Can't access account", body="I cannot login since yesterday, please help!", received_at=datetime.utcnow() - timedelta(hours=2)),
        Email(sender="bob@client.com", subject="Query about billing", body="Can you explain last invoice?", received_at=datetime.utcnow() - timedelta(hours=5)),
        Email(sender="carol@user.com", subject="Request: Feature request", body="Please add dark mode.", received_at=datetime.utcnow() - timedelta(days=1)),
    ]
    db.add_all(samples)
    db.commit()
    db.close()

if __name__ == "__main__":
    load_dummy()
    print("Loaded dummy emails.")
