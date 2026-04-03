from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from ..database import get_db
from ..models.task import Task
from ..models.user import User
from ..services.dependencies import get_current_user
from ..services.ai_service import ask_claude

router = APIRouter(prefix="/chat", tags=["chat"])

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = []

@router.post("/")
def chat(
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role == "manager":
        tasks = db.query(Task).all()
    else:
        tasks = db.query(Task).filter(Task.assignee_id == current_user.id).all()

    all_users = db.query(User).all()

    history = [{"role": m.role, "content": m.content} for m in request.history]

    response = ask_claude(current_user, tasks, all_users, history, request.message)

    return {"response": response}