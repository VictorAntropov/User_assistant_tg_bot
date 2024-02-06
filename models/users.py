from sqlalchemy import Column, DateTime, Integer, String

from core.db import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(15))
    first_name = Column(String(255))
    second_name = Column(String(255))
    email = Column(String(255))
    company = Column(String(255))
    address = Column(String(255))
    number = Column(String(255))
    qr_kod = Column(String(255))
    created_at = Column(DateTime)
