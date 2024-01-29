from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

SQLALCHEMY_DATABASE_URL = 'sqlite:///db1.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": True})

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db1 = SessionLocal()

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, nullable=False)
    title = Column(String(80), nullable=False)
    description = Column(String(80), nullable=False)
    status = Column(Boolean, nullable=False)
    is_del = Column(Boolean, nullable=False)

class TaskIn(BaseModel):
    task_id: int
    title: str # заголовок обязателен, не делаем опциональным (согласно условию)
    description: str # описание также обязательно
    status: bool # статус задачи (выполнена/не выплнена)

class TaskOut(TaskIn):
    id: int
