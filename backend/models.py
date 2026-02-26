from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    workspaces = relationship("Workspace", back_populates="owner")


class Workspace(Base):
    __tablename__ = "workspaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    papers = relationship("Paper", back_populates="workspace", cascade="all, delete")
    owner = relationship("User", back_populates="workspaces")
    conversations = relationship("Conversation", back_populates="workspace")


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    user_message = Column(Text)
    ai_response = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="conversations")

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    uploaded_at = Column(DateTime, default=datetime.utcnow)

    workspace = relationship("Workspace", back_populates="papers")