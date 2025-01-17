from sqlalchemy import Column, Integer, String, ForeignKey

from Chat_bot.core.db import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    role = ForeignKey("roles.role", ondelete="CASCADE", onupdate="CASCADE")


class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
