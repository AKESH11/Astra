# reporting_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import datetime
import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA Reporting Service")

@app.get("/")
async def health_check():
    """A simple endpoint to confirm the service is running and healthy."""
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}

# Create a directory for reports if it doesn't exist
REPORTS_DIR = "/app/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

class ReportRequest(BaseModel):
    title: str
    data: dict

@app.post("/generate_report")
async def generate_report(request: ReportRequest):
    """
    Generates a real PDF report.
    """
    logger.info(f"Generating report titled: '{request.title}'")
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Incident_Report_{timestamp}.pdf"
    filepath = os.path.join(REPORTS_DIR, filename)

    try:
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        story.append(Paragraph(request.title, styles['h1']))
        story.append(Paragraph(f"Report Generated: {datetime.datetime.now()}", styles['Normal']))
        story.append(Paragraph("<br/><br/>", styles['Normal']))
        
        # Add data from the request to the PDF
        for key, value in request.data.items():
            story.append(Paragraph(f"<b>{key.replace('_', ' ').title()}:</b> {value}", styles['Normal']))

        doc.build(story)
        logger.info(f"PDF report '{filename}' created successfully.")
        
        return {
            "status": "success",
            "filename": filename,
            "download_url": f"/reports/{filename}" 
        }
    except Exception as e:
        logger.error(f"Failed to generate PDF report: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF report.")

