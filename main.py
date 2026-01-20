from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect_db, close_db
from routes import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle startup and shutdown events."""
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="Simple CRUD API",
    description="A simple CRUD backend with FastAPI and MongoDB Atlas",
    version="1.0.0",
    lifespan=lifespan
)

# Include routes
app.include_router(router)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "API is running", "docs": "/docs"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
