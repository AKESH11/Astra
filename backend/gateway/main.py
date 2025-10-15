# gateway/main.py
import httpx
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA API Gateway")

# Allow CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Service URLs - These would be dynamically discovered in a real system (e.g., Consul, Kubernetes)
# For the hackathon, we use the service names defined in docker-compose.yml
# When running locally (not in Docker), use localhost URLs
import os
USE_DOCKER = os.getenv("USE_DOCKER", "false").lower() == "true"

if USE_DOCKER:
    NLP_SERVICE_URL = "http://nlp_service:8001/process_query"
    SIEM_SERVICE_URL = "http://siem_service:8002/query_siem"
    REPORTING_SERVICE_URL = "http://reporting_service:8003/generate_report"
    BLOCKCHAIN_SERVICE_URL = "http://blockchain_service:8004/log_action"
else:
    NLP_SERVICE_URL = "http://localhost:8001/process_query"
    SIEM_SERVICE_URL = "http://localhost:8002/query_siem"
    REPORTING_SERVICE_URL = "http://localhost:8003/generate_report"
    BLOCKCHAIN_SERVICE_URL = "http://localhost:8004/log_action"

# Asynchronous HTTP client
client = httpx.AsyncClient(timeout=30.0)

@app.post("/api/chat")
async def chat_handler(request: Request):
    """
    Main chat endpoint. Orchestrates calls to other microservices.
    1. Gets user message.
    2. Sends to NLP service to understand intent.
    3. Based on intent, calls SIEM, Reporting, or other services.
    4. Logs the action to the blockchain.
    5. Returns the final response to the user.
    """
    try:
        payload = await request.json()
        user_message = payload.get("message")
        user_id = payload.get("user_id", "anonymous")

        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty")

        logger.info(f"Received message from '{user_id}': '{user_message}'")

        # --- 1. NLP Service: Understand the user's intent ---
        logger.info("Forwarding to NLP Service for intent recognition...")
        nlp_response = await client.post(NLP_SERVICE_URL, json={"query": user_message})
        nlp_response.raise_for_status()
        nlp_data = nlp_response.json()
        
        # Parse the NLP response
        import json
        data = nlp_data.get("data", "{}")
        
        # Handle both string and dict responses
        if isinstance(data, str):
            try:
                parsed_data = json.loads(data)
            except json.JSONDecodeError:
                parsed_data = {"intent": "unknown", "entities": {}}
        else:
            parsed_data = data
        
        intent = parsed_data.get("intent", "unknown")
        entities = parsed_data.get("entities", {})
        
        logger.info(f"NLP Service identified intent: '{intent}' with entities: {entities}")

        response_data = {}

        # --- 2. Orchestration Logic based on intent ---
        if intent == "search_logs" or intent == "investigate":
            # --- Call SIEM Service ---
            logger.info("Forwarding to SIEM Service for data retrieval...")
            siem_response = await client.post(SIEM_SERVICE_URL, json={"query_params": entities})
            siem_response.raise_for_status()
            siem_data = siem_response.json()
            
            # --- Call NLP Service again for summarization ---
            logger.info("Forwarding to NLP Service for summarization...")
            summarize_url = NLP_SERVICE_URL.replace('process_query', 'summarize')
            summary_response = await client.post(
                summarize_url, 
                json={"logs": siem_data.get("hits", []), "context": user_message}
            )
            summary_response.raise_for_status()
            summary_data = summary_response.json()

            # Format logs for display
            formatted_logs = []
            for log in siem_data.get("hits", [])[:5]:
                log_str = f"{log.get('@timestamp', 'N/A')} - {log.get('message', str(log))}"
                formatted_logs.append(log_str)

            response_data = {
                "id": httpx.codes.OK,
                "sender": "astra",
                "text": "I found relevant security logs in the SIEM system.",
                "summary": summary_data.get("summary", "Analysis complete."),
                "logs": formatted_logs,
                "report_link": None
            }

        elif intent == "generate_report":
            # --- Call Reporting Service ---
            logger.info("Forwarding to Reporting Service...")
            # In a real app, you'd pass the data to be included in the report
            report_payload = {"title": "Incident Report", "data": entities} 
            report_response = await client.post(REPORTING_SERVICE_URL, json=report_payload)
            report_response.raise_for_status()
            report_data = report_response.json()
            
            response_data = {
                 "id": httpx.codes.OK,
                 "sender": "astra",
                 "text": f"Report '{report_data.get('filename')}' generated successfully.",
                 "summary": None, "logs": None,
                 "report_link": report_data.get("download_url")
            }

        else: # Default/fallback case
            response_data = {
                 "id": httpx.codes.OK,
                 "sender": "astra",
                 "text": "I can help with that. Could you be more specific about the IP, user, or timeframe?",
                 "summary": None, "logs": None, "report_link": None
            }

        # --- 3. Log the action to the Blockchain Service ---
        try:
            log_payload = {"user_id": user_id, "action": intent, "details": user_message}
            blockchain_res = await client.post(BLOCKCHAIN_SERVICE_URL, json=log_payload)
            if blockchain_res.status_code == 200:
                tx_hash = blockchain_res.json().get("transaction_hash")
                logger.info(f"Action successfully logged to blockchain. TxHash: {tx_hash}")
                if "text" in response_data:
                    response_data["text"] += f" (Audit Trail: {tx_hash[:12]}...)"
            else:
                 logger.warning("Could not log action to blockchain.")
        except Exception as e:
            logger.error(f"Failed to log to blockchain service: {e}")


        return response_data

    except httpx.RequestError as e:
        logger.error(f"HTTP Request error: {e}")
        raise HTTPException(status_code=503, detail=f"Service communication error: {e.request.url} is unavailable.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")

@app.get("/")
def read_root():
    return {"message": "ASTRA API Gateway is running."}
