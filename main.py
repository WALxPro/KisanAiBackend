from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import connect_db, close_db
from routes.admin_routes import router
from models.admin_model import AdminCreate, AdminResponse
from crud.admin_crud import create_admin, get_all_admins


from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()

app = FastAPI(
    title="Admin CRUD API",
    description="Admin backend with FastAPI and MongoDB Atlas",
    version="1.0.0",
    lifespan=lifespan
)

# ✅ CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3002",
        "https://kisanaiweb.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Admin routes only
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Admin API is running", "docs": "/docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
