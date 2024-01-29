"""Задание

Необходимо создать API для управления списком задач. Каждая задача должна содержать заголовок и описание. 
Для каждой задачи должна быть возможность указать статус (выполнена/не выполнена).

API должен содержать следующие конечные точки:
— GET /tasks — возвращает список всех задач.
— GET /tasks/{id} — возвращает задачу с указанным идентификатором.
— POST /tasks — добавляет новую задачу.
— PUT /tasks/{id} — обновляет задачу с указанным идентификатором.
— DELETE /tasks/{id} — удаляет задачу с указанным идентификатором.

Для каждой конечной точки необходимо проводить валидацию данных запроса и ответа. Для этого использовать библиотеку Pydantic."""

from fastapi import FastAPI, HTTPException
from typing import List
from models import Base, Task, TaskIn, TaskOut, engine, db1


app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.get("/tasks", response_model=List[TaskOut])
async def read_tasks(skip: int = 0, limit: int = 10):
    tasks = db1.query(Task).offset(skip).limit(limit).all()
    return tasks

@app.get("/tasks/{task_id}", response_model=TaskOut)
async def read_task(task_id: int):
    task = db1.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    return task

@app.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskIn):
    db_task = Task(**task.dict())
    db1.add(db_task)
    db1.commit()
    db1.refresh(db_task)
    return db_task

@app.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: int, task: TaskIn):
    db_task = db1.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    update_data = task.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_task, key, value)
    db1.commit()
    db1.refresh(db_task)
    return db_task

@app.delete("/tasks/{task_id}", response_model=TaskOut)
async def delete_task(task_id: int):
    db_task = db1.query(Task).filter(Task.id == task_id).first()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    db_task.is_del = True
    db1.commit()
    return db_task