"""Main entry point for the Todo REST API."""

from fastapi import FastAPI
from src.routers import todo

app = FastAPI(title="Todo REST API", root_path="/todo")

# Include routers for REST endpoints
app.include_router(todo.router)
