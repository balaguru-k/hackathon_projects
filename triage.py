from textblob import TextBlob

def triage_email(email):
    # Step 1: Set priority based on keywords
    urgent_keywords = ["urgent", "immediately", "asap", "important", "critical"]
    priority = "normal"
    if any(word in email.body.lower() for word in urgent_keywords):
        priority = "high"

    # Step 2: Sentiment analysis
    analysis = TextBlob(email.body)
    sentiment = analysis.sentiment.polarity  # -1 (negative) → +1 (positive)

    # Step 3: Generate draft reply
    if sentiment < -0.2:
        reply = f"Hi {email.sender}, sorry to hear about your issue. We’ll look into it ASAP."
    elif priority == "high":
        reply = f"Hi {email.sender}, we received your urgent request. We are taking immediate action."
    else:
        reply = f"Hi {email.sender}, thank you for your email. We’ll get back to you shortly."

    return {
        "id": email.id,
        "subject": email.subject,
        "priority": priority,
        "sentiment": sentiment,
        "draft_reply": reply
    }
