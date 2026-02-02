"""Main entry point for the Todo REST API."""

from fastapi import FastAPI
from routers import todo

app = FastAPI(title="Todo REST API")

# Include routers for REST endpoints
app.include_router(todo.router)
