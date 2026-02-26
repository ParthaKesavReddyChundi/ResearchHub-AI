from fastapi import FastAPI
from dotenv import load_dotenv

from routers import auth_router
from routers import workspace_router
from routers import paper_router

load_dotenv()

app = FastAPI(
    title="ResearchHub AI",
    version="3.2"
)

# Include routers
app.include_router(auth_router.router)
app.include_router(workspace_router.router)
app.include_router(paper_router.router)


@app.get("/")
def root():
    return {"message": "ResearchHub AI Backend Core Running"}