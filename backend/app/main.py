from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import DATA_DIR, PORT, HOST
from backend.app.routes.api import router as api_router

app = FastAPI(
    title="Organic Content OS API",
    description="AI-powered short-form video content intelligence and generation for Organic Journals",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount local data directory for static media serving (video previews, keyframes)
app.mount("/data", StaticFiles(directory=str(DATA_DIR)), name="data")

# Register API Router
app.include_router(api_router)

@app.get("/")
def root():
    return {
        "message": "Organic Content OS API is running.",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.app.main:app", host=HOST, port=PORT, reload=True)
