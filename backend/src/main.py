from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from src.chat.router import chat_router
import uvicorn

app = FastAPI(
    title="RAG App for Runpod",
    description="Welcome to RAG App for Runpod's API documentation!",
    root_path="/api/v1",
    docs_url=None,
    openapi_url="/docs/openapi.json",
    redoc_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat_router)


@app.get("/")
async def root():
    return {"message": "RAG API is running"}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, log_level="info")
