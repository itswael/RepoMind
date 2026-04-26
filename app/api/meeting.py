from fastapi import APIRouter
from app.workers.worker import enqueue_job

router = APIRouter()

@router.post("/upload")
def upload_meeting(data: dict):
    meeting_id = save_to_db(data)
    
    enqueue_job({
        "meeting_id": meeting_id,
        "transcript": data["transcript"],
        "repo": data["repo"]
    })
    
    return {"status": "processing"}

@router.get("/{meeting_id}")
def get_results(meeting_id: int):
    return fetch_results(meeting_id)