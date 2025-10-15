# blockchain_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import datetime
import hashlib
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA Blockchain Service")

# --- In-memory Blockchain for Demo ---
# In a real-world scenario, this would connect to Hyperledger Fabric or another service.
# For a hackathon, an in-memory list of blocks is a perfect proof-of-concept.
blockchain = []

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

def create_genesis_block():
    """Creates the very first block in the chain."""
    return Block(0, datetime.datetime.now().isoformat(), "Genesis Block", "0")

# Initialize the blockchain with the genesis block
if not blockchain:
    blockchain.append(create_genesis_block())

# --- Pydantic Models ---
class LogActionRequest(BaseModel):
    action_data: dict

# --- API Endpoints ---

# THIS IS THE CRUCIAL HEALTH CHECK ENDPOINT
@app.get("/")
async def health_check():
    return {"status": "ok"}

@app.post("/log_action")
async def log_action(request: LogActionRequest):
    """
    Receives an action, creates a new block, and adds it to the chain.
    """
    try:
        previous_block = blockchain[-1]
        new_index = previous_block.index + 1
        new_timestamp = datetime.datetime.now().isoformat()
        new_block = Block(new_index, new_timestamp, request.action_data, previous_block.hash)
        blockchain.append(new_block)
        
        logger.info(f"Action logged to blockchain. New block index: {new_block.index}, Hash: {new_block.hash}")
        
        return {
            "status": "success",
            "message": "Action logged to blockchain.",
            "block_index": new_block.index,
            "transaction_hash": new_block.hash
        }
    except Exception as e:
        logger.error(f"Failed to log action to blockchain: {e}")
        raise HTTPException(status_code=500, detail="Failed to log action to blockchain.")

@app.get("/chain")
async def get_chain():
    """Returns the entire current blockchain."""
    return [block.__dict__ for block in blockchain]

