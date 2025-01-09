from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str
    custom_dataset: bool = False


class ChatResponse(BaseModel):
    message: str
    timestamp: datetime = datetime.now()
    status: str = "success"
    error: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "message": "Hello! How can I help you today?",
                "timestamp": "2024-01-01T12:00:00",
                "status": "success",
                "error": None,
            }
        }
