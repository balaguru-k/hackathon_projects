from pydantic import BaseModel
from datetime import datetime

class Email(BaseModel):
    id: int
    sender: str
    subject: str
    body: str
    received_at: datetime

def get_emails():
    return [
        Email(
            id=1,
            sender="alice@example.com",
            subject="Support: Can't access account",
            body="I cannot login since yesterday, please help!",
            received_at=datetime.now()
        ),
        Email(
            id=2,
            sender="bob@client.com",
            subject="Query about billing",
            body="Can you explain last invoice?",
            received_at=datetime.now()
        ),
        Email(
            id=3,
            sender="carol@user.com",
            subject="Request: Feature request",
            body="Please add dark mode.",
            received_at=datetime.now()
        ),
    ]
