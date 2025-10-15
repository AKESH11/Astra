# reporting_service/main_local.py - Simplified local version
from fastapi import FastAPI
from pydantic import BaseModel
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA Reporting Service (Local Mock)")

class ReportRequest(BaseModel):
    title: str
    data: dict

@app.get("/")
async def health_check():
    """Health check endpoint"""
    return {"status": "ok", "message": "Reporting Service (Local Mock) is running"}

@app.post("/generate_report")
async def generate_report(request: ReportRequest):
    """Mock report generation"""
    logger.info(f"Generating report: {request.title}")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"incident_report_{timestamp}.pdf"
    
    return {
        "status": "success",
        "filename": filename,
        "download_url": f"/reports/{filename}",
        "message": "Report generated successfully (mock)"
    }
