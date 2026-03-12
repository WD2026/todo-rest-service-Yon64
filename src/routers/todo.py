"""REST endpoints for todos."""

from fastapi import APIRouter, HTTPException, Request, Response, status
from src.models import Todo, TodoCreate
from src.persistence import TodoDao
from src import logging_config

dao = TodoDao("todo_data.json")

router = APIRouter(
    prefix="/todos",
    tags=["Todos"]
)

logger = logging_config.get_logger(__name__)    


@router.get("/", response_model=list[Todo])
def get_todos():
    logger.info("Getting all todos")
    return dao.get_all()


@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: TodoCreate, request: Request, response: Response):
    created = dao.save(todo)
    logger.info("Todo created", todo_id=created.id, text=created.text)
    response.headers["Location"] = f"/todos/{created.id}"
    return created


@router.get("/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todo = dao.get(todo_id)
    if not todo:
        # NEW: add structured logging. 
        logger.warning("Todo not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@router.put("/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):
    existing = dao.get(todo_id)
    if not existing:
        logger.warning("Failed to update todo: ID not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")

    updated = Todo(id=todo_id, text=todo.text, done=todo.done)
    result = dao.update(updated)
    logger.info("Todo modified", todo_id=todo_id)
    return result


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    if not dao.delete(todo_id):
        logger.error("Failed to delete todo: ID not found", todo_id=todo_id)
        raise HTTPException(status_code=404, detail="Todo not found")
    logger.info("Todo deleted", todo_id=todo_id)
    return


@router.options("/")
def todos_options(response: Response):
    response.headers["Allow"] = "GET,POST,OPTIONS"
    return response


@router.options("/{todo_id}")
def todo_options(todo_id: int, response: Response):
    response.headers["Allow"] = "GET,PUT,DELETE,OPTIONS"
    return response
