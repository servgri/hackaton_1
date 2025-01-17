from sqlalchemy import Column, Integer, String, LargeBinary
from Chat_bot.core.db import Base


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    data = Column(LargeBinary, nullable=False)
