def generate_reply(email):
    """Very simple reply generator."""
    if "billing" in email.subject.lower():
        return "Hello, we are looking into your billing query and will get back soon."
    elif "account" in email.subject.lower():
        return "Hello, please reset your password using the link we provided."
    elif "feature" in email.subject.lower():
        return "Thanks for your suggestion! We value your feedback."
    else:
        return "Thanks for reaching out. Our team will respond shortly."
