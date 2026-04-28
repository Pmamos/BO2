import os
import time
from celery import Celery

# Pobieramy adres z Dockera. Jeśli odpalisz to bez Dockera, domyślnie użyje localhost.
REDIS_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "farm_worker",
    broker=REDIS_URL,
    backend=REDIS_URL
)

@celery_app.task
def run_heavy_simulation(years: int, fields: int):
    print(f"WORKER: Zaczynam ciężką symulację dla {fields} pól i {years} lat...")
    for i in range(1, 11):
        time.sleep(1)
        print(f"WORKER: Postęp {i * 10}%...")
    print("WORKER: Zrobione!")
    return {"status": "success", "profit": 150000.50}