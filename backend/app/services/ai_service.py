from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def build_workspace_context(user, tasks, all_users):
    context = f"""You are an AI assistant for Workforce AI, a team task management system.
You have access to real-time workspace data. Answer questions based on this data only.

CURRENT USER:
- Name: {user.full_name}
- Role: {user.role}
- ID: {user.id}

TEAM MEMBERS:
"""
    for u in all_users:
        context += f"- {u.full_name} (ID: {u.id}, Role: {u.role})\n"

    context += "\nALL TASKS:\n"
    if not tasks:
        context += "No tasks found.\n"
    else:
        for task in tasks:
            assignee_name = next((u.full_name for u in all_users if u.id == task.assignee_id), "Unassigned")
            creator_name = next((u.full_name for u in all_users if u.id == task.creator_id), "Unknown")
            due = task.due_date.strftime("%Y-%m-%d") if task.due_date else "No due date"
            context += f"""
- [{task.id}] {task.title}
  Status: {task.status} | Priority: {task.priority} | Due: {due}
  Assigned to: {assignee_name} | Created by: {creator_name}
  Description: {task.description or 'None'}
"""

    context += """
INSTRUCTIONS:
- Answer questions about tasks, team workload, and productivity
- Be concise and helpful
- If asked who is overloaded, check who has the most in-progress or todo tasks
- If asked for a summary, be brief and structured
- Do not make up data that isn't in the context above
"""
    return context


def ask_claude(user, tasks, all_users, conversation_history: list, user_message: str) -> str:
    system_prompt = build_workspace_context(user, tasks, all_users)

    messages = conversation_history + [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        max_tokens=1000,
        messages=[{"role": "system", "content": system_prompt}] + messages
    )

    return response.choices[0].message.content