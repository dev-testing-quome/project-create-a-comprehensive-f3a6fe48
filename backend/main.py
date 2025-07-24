import uvicorn
from fastapi import FastAPI, Request, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import os
from sqlalchemy.orm import Session

from .database import SessionLocal, engine
from . import models
from . import schemas
#from .routers import users, trades # Add your routers here

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"] # Update with your allowed origins in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check
@app.get("/health")
def health_check():
    return {"status": "OK"}

# Mount static files for frontend
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

    @app.get("/{file_path:path}")
    async def serve_frontend(file_path: str):
        if file_path.startswith("api/") or file_path.startswith("static/") :
            return None  # Let API routes handle it
        static_file = os.path.join("static", file_path)
        if os.path.isfile(static_file):
            return FileResponse(static_file)
        return FileResponse("static/index.html")  # SPA routing

#Include your routers here
#app.include_router(users.router)
#app.include_router(trades.router)

@app.exception_handler(Exception)
def handle_exception(request: Request, exc: Exception):
    return HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
