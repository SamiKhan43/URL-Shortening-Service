from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime, timezone

from database import Base, engine, SessionLocal
from models import ShortUrl
from utils import generate_unique_short_code

app = FastAPI()

Base.metadata.create_all(bind=engine)


class URLCreate(BaseModel):
    url: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def home_page():
    return {"message": "welcome to the URL Shortening Service"}


@app.post("/shorten", status_code=201)
def create_short_url(data: URLCreate, db=Depends(get_db)):
    short_code = generate_unique_short_code(db)
    now = datetime.now(timezone.utc)

    new_short_url = ShortUrl(
        url=data.url,
        short_code=short_code,
        created_at=now,
        updated_at=now,
        access_count=0
    )

    db.add(new_short_url)
    db.commit()
    db.refresh(new_short_url)

    return new_short_url


@app.get("/shorten/{ShortCode}")
def get_short_url(ShortCode: str, db=Depends(get_db)):
    short_url = db.query(ShortUrl).filter(
        ShortUrl.short_code == ShortCode
    ).first()

    if not short_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    short_url.access_count += 1
    db.commit()

    return short_url


@app.put("/shorten/{ShortCode}")
def update_short_url(
    ShortCode: str,
    updated: URLCreate,
    db=Depends(get_db)
):
    short_url = db.query(ShortUrl).filter(
        ShortUrl.short_code == ShortCode
    ).first()

    if not short_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    short_url.url = updated.url
    short_url.updated_at = datetime.now(timezone.utc)

    db.commit()

    return short_url


@app.delete("/shorten/{ShortCode}", status_code=204)
def delete_short_url(ShortCode: str, db=Depends(get_db)):
    short_url = db.query(ShortUrl).filter(
        ShortUrl.short_code == ShortCode
    ).first()

    if not short_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    db.delete(short_url)
    db.commit()

    return


@app.get("/shorten/{ShortCode}/stats")
def get_short_url_stats(ShortCode: str, db=Depends(get_db)):
    short_url = db.query(ShortUrl).filter(
        ShortUrl.short_code == ShortCode
    ).first()

    if not short_url:
        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    return {
        "short_code": short_url.short_code,
        "url": short_url.url,
        "access_count": short_url.access_count,
        "created_at": short_url.created_at,
        "updated_at": short_url.updated_at
    }
    