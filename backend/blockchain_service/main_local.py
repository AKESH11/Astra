# blockchain_service/main_local.py - Simplified local version
from fastapi import FastAPI
from pydantic import BaseModel
import logging
import hashlib
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA Blockchain Service (Local Mock)")

class LogAction(BaseModel):
    user_id: str
    action: str
    details: str

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Blockchain Service (Local Mock) is running"}

@app.post("/log_action")
async def log_action(request: LogAction):
    """Mock blockchain logging - generates a fake transaction hash"""
    logger.info(f"Logging action to blockchain: {request.action} by {request.user_id}")
    
    # Generate a mock transaction hash
    data = f"{request.user_id}{request.action}{request.details}{time.time()}"
    tx_hash = hashlib.sha256(data.encode()).hexdigest()
    
    return {
        "status": "success",
        "transaction_hash": tx_hash,
        "message": "Action logged to blockchain (mock)"
    }
