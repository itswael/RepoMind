# app/services/pipeline/processor.py

from app.utils.chunker import chunk_text
from app.services.llm.task_extractor import extract_tasks
from app.services.llm.validator import validate_task
from app.services.github.issue_creator import create_issue

def process_meeting(data):
    transcript = data["transcript"]
    
    chunks = chunk_text(transcript)
    
    all_tasks = []
    
    for chunk in chunks:
        tasks = extract_tasks(chunk)
        
        for task in tasks:
            if validate_task(task):
                all_tasks.append(task)
    
    for task in all_tasks:
        create_issue(data["repo"], task)
    
    return all_tasks