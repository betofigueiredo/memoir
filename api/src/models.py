from core.settings import settings
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import BIGINT, TEXT
from sqlalchemy.orm import relationship


class User(settings.DB_BASE_MODEL):
    __tablename__ = "user"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200))
    notes = relationship("Note", back_populates="user", lazy="subquery")


class Note(settings.DB_BASE_MODEL):
    __tablename__ = "note"

    id = Column(BIGINT, primary_key=True, index=True, autoincrement=True)
    content = Column(TEXT)
    user_id = Column(BIGINT, ForeignKey("user.id"))
    user = relationship("User", back_populates="notes", lazy="subquery")
