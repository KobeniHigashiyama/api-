from sqlalchemy import Column, Integer, String, Boolean, ForeignKey,DateTime
from sqlalchemy.orm import relationship
from app.db.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # Роль пользователя: "user", "admin"

    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    is_completed = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    priority = Column(Integer, default=3)  # Приоритет задачи: 1 - высокий, 3 - средний, 5 - низкий
    deadline = Column(DateTime, default=None)  
    assigned_user_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Пользователь, которому назначена задача



    owner = relationship("User", back_populates="tasks")
    assigned_user = relationship("User", foreign_keys=[assigned_user_id]) 
