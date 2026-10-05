import secrets
import string
from models import ShortUrl

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    short_code = "".join(secrets.choice(characters) for _ in range(length))
    return short_code

def generate_unique_short_code(db):
    while True:
        code = generate_short_code()
        existing = db.query(ShortUrl).filter(ShortUrl.short_code == code).first()
        if not existing:
            return code