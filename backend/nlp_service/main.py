# nlp_service/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
from openai import OpenAI
from typing import List, Dict, Any
from ai_analyzer import AISecurityAnalyzer

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="ASTRA NLP Service - Enhanced with Advanced AI")

# --- Configuration from docker-compose.yml ---
API_BASE = os.getenv("OPENAI_API_BASE", "http://host.docker.internal:11434/v1")
LLM_MODEL = os.getenv("LLM_MODEL", "llama3")
client = OpenAI(base_url=API_BASE, api_key="not-needed")

# --- Pydantic Models ---
class QueryRequest(BaseModel):
    query: str

class SummarizeRequest(BaseModel):
    logs: List[Dict[str, Any]]
    context: str

# --- API Endpoints ---

@app.get("/")
async def health_check():
    """A simple endpoint to confirm the service is running and healthy."""
    logger.info("Health check endpoint was called.")
    return {"status": "ok"}

@app.post("/process_query")
async def process_query(request: QueryRequest):
    """Takes a raw query and uses an LLM to extract intent and entities."""
    logger.info(f"Processing query with LLM: '{request.query}'")
    system_prompt = "You are an expert cybersecurity analyst's assistant. Convert the user's query into a structured JSON object with 'intent' and 'entities'. Respond with only the JSON."
    
    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.query}
            ],
            response_format={"type": "json_object"}
        )
        llm_result = response.choices[0].message.content
        logger.info(f"LLM Response: {llm_result}")
        return {"status": "success", "data": llm_result}
    except Exception as e:
        logger.error(f"LLM API call failed: {e}")
        # Provide a simple fallback if the LLM fails
        import json
        query_lower = request.query.lower()
        
        # Simple rule-based intent detection
        intent = "search_logs"
        if "report" in query_lower or "generate" in query_lower:
            intent = "generate_report"
        elif "investigate" in query_lower or "hunt" in query_lower or "scan" in query_lower or "look for" in query_lower:
            intent = "investigate"
        
        entities = {"raw_text": request.query}
        
        # Extract simple patterns
        if "ip" in query_lower or any(char.isdigit() and "." in request.query for char in request.query):
            entities["type"] = "ip_investigation"
        
        fallback_data = {"intent": intent, "entities": entities}
        logger.info(f"Fallback intent detection: {fallback_data}")
        return {"status": "fallback", "data": json.dumps(fallback_data)}

@app.post("/summarize")
async def summarize_logs(request: SummarizeRequest):
    """Takes logs and generates a human-readable summary."""
    logger.info(f"Summarizing {len(request.logs)} logs.")
    system_prompt = "You are a senior cybersecurity incident responder. Analyze these logs and write a brief, clear, human-readable summary telling the story of what happened."
    
    log_string = "\n".join([str(log) for log in request.logs])
    user_prompt = f"Context: {request.context}\n\nPlease summarize these logs:\n{log_string}"
    
    try:
        response = client.chat.completions.create(model=LLM_MODEL, messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}])
        summary = response.choices[0].message.content
        logger.info("Summary generated successfully.")
        return {"status": "success", "summary": summary}
    except Exception as e:
        logger.error(f"LLM API call for summarization failed: {e}")
        # Provide a fallback summary when LLM is unavailable
        fallback_summary = f"Security Analysis Summary:\n\nAnalyzed {len(request.logs)} security events related to: {request.context}\n\n"
        
        if request.logs:
            # Use Advanced AI Analyzer
            threat_analysis = AISecurityAnalyzer.threat_severity_scoring(request.logs)
            iocs = AISecurityAnalyzer.extract_iocs(request.logs)
            prediction = AISecurityAnalyzer.predict_next_attack_vector(request.logs)
            executive_summary = AISecurityAnalyzer.generate_executive_summary(request.logs, request.context)
            
            # Build comprehensive summary
            fallback_summary = f"🔍 AI SECURITY ANALYSIS\n\n"
            fallback_summary += f"📊 THREAT ASSESSMENT:\n"
            fallback_summary += f"   • Risk Score: {threat_analysis['risk_score']}/100\n"
            fallback_summary += f"   • Threat Level: {threat_analysis['threat_level']}\n"
            fallback_summary += f"   • Events Analyzed: {len(request.logs)}\n\n"
            
            if threat_analysis['factors']:
                fallback_summary += f"🎯 KEY FINDINGS:\n"
                for factor in threat_analysis['factors'][:3]:
                    fallback_summary += f"   • {factor}\n"
                fallback_summary += "\n"
            
            if iocs:
                fallback_summary += f"🔎 INDICATORS OF COMPROMISE (IOCs):\n"
                if iocs.get('ip_addresses'):
                    fallback_summary += f"   • Suspicious IPs: {', '.join(iocs['ip_addresses'][:3])}\n"
                if iocs.get('usernames'):
                    fallback_summary += f"   • Affected Users: {', '.join(iocs['usernames'][:3])}\n"
                if iocs.get('processes'):
                    fallback_summary += f"   • Suspicious Processes: {', '.join(iocs['processes'][:2])}\n"
                fallback_summary += "\n"
            
            fallback_summary += f"🔮 PREDICTIVE ANALYSIS:\n"
            fallback_summary += f"   • Current Attack Phase: {prediction['current_phase']}\n"
            fallback_summary += f"   • Predicted Next Steps: {', '.join(prediction['predicted_next_steps'])}\n"
            fallback_summary += f"   • Probability: {prediction['probability']}\n\n"
            
            fallback_summary += f"✅ RECOMMENDED ACTIONS:\n{threat_analysis['recommendation']}\n\n"
            
            fallback_summary += f"📋 EXECUTIVE SUMMARY:\n{executive_summary}"
        else:
            fallback_summary += "No specific security events found matching the query criteria."
        
        logger.info("Returning enhanced AI summary (LLM unavailable)")
        return {"status": "success", "summary": fallback_summary}

@app.post("/threat_analysis")
async def advanced_threat_analysis(request: SummarizeRequest):
    """Advanced threat analysis with risk scoring and predictions"""
    logger.info(f"Performing advanced threat analysis on {len(request.logs)} logs.")
    
    threat_score = AISecurityAnalyzer.threat_severity_scoring(request.logs)
    iocs = AISecurityAnalyzer.extract_iocs(request.logs)
    timeline = AISecurityAnalyzer.attack_timeline(request.logs)
    prediction = AISecurityAnalyzer.predict_next_attack_vector(request.logs)
    confidence = AISecurityAnalyzer.ai_confidence_score(request.context, request.logs)
    
    return {
        "status": "success",
        "threat_assessment": threat_score,
        "indicators_of_compromise": iocs,
        "attack_timeline": timeline,
        "predictive_analysis": prediction,
        "ai_confidence": confidence
    }

@app.post("/extract_iocs")
async def extract_indicators(request: SummarizeRequest):
    """Extract Indicators of Compromise from logs"""
    logger.info("Extracting IOCs from logs")
    iocs = AISecurityAnalyzer.extract_iocs(request.logs)
    return {"status": "success", "iocs": iocs}

