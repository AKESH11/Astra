# ASTRA - Running Services Summary

## ✅ All Services Are Running Successfully!

### Service Status:

1. **API Gateway** - Port 8000
   - Status: ✅ Running
   - URL: http://localhost:8000
   - Purpose: Main orchestration layer, handles all frontend requests

2. **NLP Service** - Port 8001
   - Status: ✅ Running
   - URL: http://localhost:8001
   - Purpose: Natural language processing for query understanding and summarization

3. **SIEM Service (Mock)** - Port 8002
   - Status: ✅ Running
   - URL: http://localhost:8002
   - Purpose: Returns mock security logs for testing

4. **Reporting Service (Mock)** - Port 8003
   - Status: ✅ Running
   - URL: http://localhost:8003
   - Purpose: Generates incident reports

5. **Blockchain Service (Mock)** - Port 8004
   - Status: ✅ Running
   - URL: http://localhost:8004
   - Purpose: Logs audit trail with mock blockchain hashes

### Frontend:
- File: `frontend/index.html`
- Open this file in your browser to access the ASTRA interface
- The frontend connects to: http://localhost:8000/api/chat

### What Was Fixed:

1. **Service URLs**: Modified gateway to use `localhost` instead of Docker service names
2. **NLP Service Port**: Moved from 8003 to 8001 (correct port per docker-compose)
3. **Mock Services**: Created local mock versions for SIEM, Reporting, and Blockchain services
4. **API Communication**: Fixed JSON payload structures between services
5. **Response Format**: Fixed summary and log formatting for frontend display

### How to Test:

1. Open `frontend/index.html` in your web browser
2. Try these test queries:
   - "Show me failed login attempts"
   - "Look for signs of ransomware"
   - "Generate an incident report"
   - "Scan for lateral movement activity"

### Notes:

- All services are running in **reload mode** (will auto-restart on code changes)
- Mock services return dummy data for testing without requiring Elasticsearch or other dependencies
- To stop all services: Press CTRL+C in each terminal window

### Troubleshooting:

If you still get "Failed to fetch" errors:
1. Check that all services are running (ports 8000-8004)
2. Open browser console (F12) to see detailed error messages
3. Verify CORS is enabled (already configured in gateway)
4. Make sure you're opening the HTML file via browser (not just viewing source)
