# AI Enhancement Features for ASTRA

## Additional AI capabilities to demonstrate

from typing import List, Dict, Any
import re
from datetime import datetime, timedelta

class AISecurityAnalyzer:
    """Advanced AI-powered security analysis features"""
    
    @staticmethod
    def threat_severity_scoring(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate threat severity score based on multiple factors
        Returns: Risk score (0-100) and threat level
        """
        score = 0
        factors = []
        
        for log in logs:
            # Check for critical events
            if isinstance(log, dict):
                event_type = log.get('event', {}).get('action', '')
                outcome = log.get('event', {}).get('outcome', '')
                
                # High severity indicators
                if 'ransomware' in str(log).lower() or 'encryption' in event_type:
                    score += 30
                    factors.append("Ransomware indicators detected")
                
                if 'exfiltration' in str(log).lower() or 'data_transfer' in event_type:
                    score += 25
                    factors.append("Data exfiltration detected")
                
                if 'lateral_movement' in event_type:
                    score += 20
                    factors.append("Lateral movement detected")
                
                if outcome == 'failure' and 'login' in event_type:
                    score += 5
                    factors.append("Multiple failed login attempts")
                
                if 'privilege_escalation' in event_type:
                    score += 35
                    factors.append("Privilege escalation detected")
        
        # Determine threat level
        if score >= 70:
            threat_level = "CRITICAL"
            color = "red"
        elif score >= 50:
            threat_level = "HIGH"
            color = "orange"
        elif score >= 30:
            threat_level = "MEDIUM"
            color = "yellow"
        else:
            threat_level = "LOW"
            color = "green"
        
        return {
            "risk_score": min(score, 100),
            "threat_level": threat_level,
            "color": color,
            "factors": factors,
            "recommendation": AISecurityAnalyzer._get_recommendation(threat_level)
        }
    
    @staticmethod
    def _get_recommendation(threat_level: str) -> str:
        """Get recommended actions based on threat level"""
        recommendations = {
            "CRITICAL": "IMMEDIATE ACTION REQUIRED: Isolate affected systems, activate incident response team, notify management.",
            "HIGH": "URGENT: Investigate immediately, prepare containment measures, alert security team.",
            "MEDIUM": "MONITOR: Continue investigation, implement additional logging, review security controls.",
            "LOW": "ROUTINE: Log for future reference, continue normal monitoring."
        }
        return recommendations.get(threat_level, "Review and assess")
    
    @staticmethod
    def extract_iocs(logs: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Extract Indicators of Compromise (IOCs) from logs
        Returns: Dictionary with IPs, domains, file hashes, etc.
        """
        iocs = {
            "ip_addresses": set(),
            "domains": set(),
            "file_paths": set(),
            "usernames": set(),
            "processes": set()
        }
        
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        domain_pattern = r'\b(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}\b'
        
        for log in logs:
            if isinstance(log, dict):
                # Extract IPs
                if 'source' in log and 'ip' in log['source']:
                    iocs["ip_addresses"].add(log['source']['ip'])
                if 'destination' in log and 'ip' in log['destination']:
                    iocs["ip_addresses"].add(log['destination']['ip'])
                
                # Extract file paths
                if 'file' in log and 'path' in log['file']:
                    iocs["file_paths"].add(log['file']['path'])
                
                # Extract usernames
                if 'user' in log and 'name' in log['user']:
                    iocs["usernames"].add(log['user']['name'])
                
                # Extract processes
                if 'process' in log and 'name' in log['process']:
                    iocs["processes"].add(log['process']['name'])
                
                # Search in message field
                message = log.get('message', '')
                iocs["ip_addresses"].update(re.findall(ip_pattern, message))
                iocs["domains"].update(re.findall(domain_pattern, message))
        
        # Convert sets to sorted lists
        return {k: sorted(list(v)) for k, v in iocs.items() if v}
    
    @staticmethod
    def attack_timeline(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Create a chronological attack timeline from logs
        Returns: Ordered list of events with timestamps
        """
        timeline = []
        
        for log in logs:
            if isinstance(log, dict):
                timestamp = log.get('@timestamp', 'Unknown')
                action = log.get('event', {}).get('action', 'Unknown')
                message = log.get('message', str(log))
                
                timeline.append({
                    "timestamp": timestamp,
                    "action": action,
                    "description": message
                })
        
        # Sort by timestamp
        try:
            timeline.sort(key=lambda x: x['timestamp'])
        except:
            pass
        
        return timeline
    
    @staticmethod
    def predict_next_attack_vector(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Predict likely next steps in an attack based on current activity
        """
        attack_patterns = {
            "reconnaissance": ["Initial Access", "Credential Dumping"],
            "initial_access": ["Execution", "Persistence"],
            "execution": ["Privilege Escalation", "Defense Evasion"],
            "privilege_escalation": ["Lateral Movement", "Credential Access"],
            "lateral_movement": ["Collection", "Exfiltration"],
            "collection": ["Exfiltration", "Impact"]
        }
        
        # Analyze current attack phase
        current_phase = "reconnaissance"
        for log in logs:
            if isinstance(log, dict):
                action = log.get('event', {}).get('action', '').lower()
                if 'lateral' in action:
                    current_phase = "lateral_movement"
                elif 'privilege' in action or 'escalation' in action:
                    current_phase = "privilege_escalation"
                elif 'login' in action or 'access' in action:
                    current_phase = "initial_access"
        
        next_steps = attack_patterns.get(current_phase, ["Unknown"])
        
        return {
            "current_phase": current_phase.replace('_', ' ').title(),
            "predicted_next_steps": next_steps,
            "probability": "High" if len(logs) > 3 else "Medium",
            "mitigation": f"Monitor for {', '.join(next_steps)} activities. Strengthen defenses in these areas."
        }
    
    @staticmethod
    def generate_executive_summary(logs: List[Dict[str, Any]], context: str) -> str:
        """
        Generate a concise executive summary for management
        """
        threat_score = AISecurityAnalyzer.threat_severity_scoring(logs)
        iocs = AISecurityAnalyzer.extract_iocs(logs)
        
        summary = f"""
EXECUTIVE SUMMARY - SECURITY INCIDENT

Incident Type: {context}
Threat Level: {threat_score['threat_level']} (Risk Score: {threat_score['risk_score']}/100)
Events Analyzed: {len(logs)}
Time of Detection: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

KEY FINDINGS:
"""
        for idx, factor in enumerate(threat_score['factors'][:3], 1):
            summary += f"\n{idx}. {factor}"
        
        if iocs.get('ip_addresses'):
            summary += f"\n\nSUSPICIOUS IP ADDRESSES: {', '.join(list(iocs['ip_addresses'])[:3])}"
        
        if iocs.get('usernames'):
            summary += f"\nAFFECTED USERS: {', '.join(list(iocs['usernames'])[:3])}"
        
        summary += f"\n\nRECOMMENDED ACTION:\n{threat_score['recommendation']}"
        
        summary += f"\n\nFull technical report available in the incident documentation."
        
        return summary.strip()
    
    @staticmethod
    def ai_confidence_score(query: str, results: List[Dict]) -> Dict[str, Any]:
        """
        Calculate AI confidence in the results
        """
        # Factors that affect confidence
        confidence = 85  # Base confidence
        
        # Lower confidence for vague queries
        if len(query.split()) < 3:
            confidence -= 10
        
        # Higher confidence with more results
        if len(results) > 5:
            confidence += 5
        elif len(results) == 0:
            confidence -= 30
        
        # Adjust based on result consistency
        if len(results) > 0:
            # Check if results have similar patterns
            event_types = set()
            for r in results:
                if isinstance(r, dict) and 'event' in r:
                    event_types.add(r['event'].get('action', ''))
            
            if len(event_types) == 1:
                confidence += 10  # Very consistent results
        
        confidence = max(0, min(100, confidence))
        
        if confidence >= 90:
            assessment = "Very High - Results are highly relevant"
        elif confidence >= 75:
            assessment = "High - Results match query intent well"
        elif confidence >= 60:
            assessment = "Medium - Some results may be tangential"
        else:
            assessment = "Low - Consider refining your query"
        
        return {
            "confidence_score": confidence,
            "assessment": assessment,
            "explanation": f"Based on query clarity, result quantity ({len(results)}), and pattern consistency"
        }
