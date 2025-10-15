# siem_service/main_local.py - Simplified local version without Elasticsearch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA SIEM Connector Service (Local Mock)")

class QueryParams(BaseModel):
    query_params: dict

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "SIEM Service (Local Mock) is running"}

@app.post("/query_siem")
async def query_siem(params: QueryParams):
    """Mock SIEM query that returns sample security logs"""
    query_info = params.query_params
    logger.info(f"Received SIEM query request with params: {query_info}")
    
    # Generate mock security logs
    mock_logs = [
        {
            "@timestamp": "2025-10-15T10:30:45.123Z",
            "event": {
                "action": "login_attempt",
                "outcome": "failure",
                "category": "authentication"
            },
            "source": {"ip": "192.168.1.100", "port": 54321},
            "destination": {"ip": "10.0.0.50", "port": 22},
            "user": {"name": "admin"},
            "message": "Failed SSH login attempt from 192.168.1.100"
        },
        {
            "@timestamp": "2025-10-15T10:31:12.456Z",
            "event": {
                "action": "login_attempt",
                "outcome": "failure",
                "category": "authentication"
            },
            "source": {"ip": "192.168.1.100", "port": 54322},
            "destination": {"ip": "10.0.0.50", "port": 22},
            "user": {"name": "root"},
            "message": "Failed SSH login attempt from 192.168.1.100"
        },
        {
            "@timestamp": "2025-10-15T10:32:05.789Z",
            "event": {
                "action": "firewall_block",
                "outcome": "success",
                "category": "network"
            },
            "source": {"ip": "192.168.1.100", "port": 54323},
            "destination": {"ip": "10.0.0.50", "port": 3389},
            "message": "Firewall blocked RDP connection attempt from suspicious IP"
        },
        {
            "@timestamp": "2025-10-15T10:33:20.123Z",
            "event": {
                "action": "file_access",
                "outcome": "success",
                "category": "file"
            },
            "user": {"name": "suspicious_user"},
            "file": {"path": "/etc/passwd"},
            "message": "Unauthorized file access attempt detected"
        },
        {
            "@timestamp": "2025-10-15T10:34:15.456Z",
            "event": {
                "action": "port_scan",
                "outcome": "detected",
                "category": "network"
            },
            "source": {"ip": "192.168.1.100"},
            "destination": {"ip": "10.0.0.0/24"},
            "message": "Port scan detected from 192.168.1.100 targeting internal network"
        }
    ]
    
    # Filter based on query
    raw_text = query_info.get("raw_text", "").lower()
    if "failed login" in raw_text or "login" in raw_text:
        mock_logs = [log for log in mock_logs if "login" in log.get("message", "").lower()]
    elif "ransomware" in raw_text:
        mock_logs = [
            {
                "@timestamp": "2025-10-15T10:35:00.000Z",
                "event": {"action": "file_encryption", "outcome": "success", "category": "malware"},
                "user": {"name": "compromised_user"},
                "file": {"path": "C:/Users/victim/Documents/important.docx.encrypted"},
                "process": {"name": "ransomware.exe"},
                "message": "Suspicious file encryption activity detected - possible ransomware"
            },
            {
                "@timestamp": "2025-10-15T10:36:00.000Z",
                "event": {"action": "ransom_note_creation", "outcome": "success", "category": "malware"},
                "file": {"path": "C:/README_DECRYPT.txt"},
                "message": "Ransom note file created on system"
            }
        ]
    
    logger.info(f"Returning {len(mock_logs)} mock log entries")
    return {"status": "success", "hits": mock_logs, "total": len(mock_logs)}
