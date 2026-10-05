from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class ShortUrl(Base):
    __tablename__ = "short_urls"

    id = Column(Integer, primary_key=True)
    url = Column(String)
    short_code = Column(String, unique = True , index = True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    access_count = Column(Integer)