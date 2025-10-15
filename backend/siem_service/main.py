# siem_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from elasticsearch import Elasticsearch, NotFoundError, ConnectionError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA SIEM Connector Service")

try:
    es_client = Elasticsearch("http://elasticsearch:9200")
    logger.info("Initializing connection to Elasticsearch...")
    # A better way to check the connection is to ask for info.
    if not es_client.info():
         raise ConnectionError("Could not get cluster info from Elasticsearch.")
    logger.info("Successfully connected to Elasticsearch.")
except ConnectionError as e:
    logger.error(f"Failed to connect to Elasticsearch on startup: {e}")
    es_client = None

class QueryParams(BaseModel):
    query_params: dict

@app.post("/query_siem")
async def query_siem(params: QueryParams):
    if not es_client:
        raise HTTPException(status_code=503, detail="SIEM service is not connected to Elasticsearch.")

    query_info = params.query_params
    logger.info(f"Received SIEM query request with params: {query_info}")
    
    # ... (the rest of the query building logic remains the same)
    search_body = {
        "query": { "bool": { "must": [] } },
        "size": 100,
        "sort": [{"@timestamp": "desc"}]
    }

    raw_text = query_info.get("raw_text", "")
    if "failed logins" in raw_text:
        search_body["query"]["bool"]["must"].append({"match": {"event.outcome": "failure"}})
    
    if query_info.get("ip_address"):
        search_body["query"]["bool"]["must"].append({
            "multi_match": { "query": query_info.get("ip_address"), "fields": ["source.ip", "destination.ip", "client.ip"]}
        })

    logger.info(f"Executing Elasticsearch query: {search_body}")

    try:
        response = es_client.search(index="security-logs-*", body=search_body)
        hits = [doc['_source'] for doc in response['hits']['hits']]
        total = response['hits']['total']['value']
        logger.info(f"Query successful. Found {total} matching documents.")
        return {"status": "success", "hits": hits, "total": total}
    except NotFoundError:
        logger.warning("No security-logs-* index found.")
        return {"status": "success", "hits": [], "total": 0}
    except Exception as e:
        logger.error(f"Error querying Elasticsearch: {e}")
        raise HTTPException(status_code=500, detail=str(e))

