from redis import Redis
from rq import Queue
from app.services.pipeline.processor import process_meeting

redis_conn = Redis()
queue = Queue(connection=redis_conn)

def enqueue_job(data):
    queue.enqueue(process_meeting, data)