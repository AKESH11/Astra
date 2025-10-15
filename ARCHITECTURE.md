# 🏗️ ASTRA System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Modern Web Frontend (React + TailwindCSS)                 │    │
│  │  • Conversational Chat Interface                            │    │
│  │  • Real-time Response Display                               │    │
│  │  • Dark Theme Optimized for SOC                             │    │
│  │  • Responsive Design (Desktop/Mobile)                       │    │
│  └──────────────────────┬─────────────────────────────────────┘    │
└─────────────────────────┼─────────────────────────────────────────┘
                          │ HTTP/REST API
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY LAYER                                │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │  Gateway Service (FastAPI + CORS)                          │    │
│  │  • Request Orchestration                                    │    │
│  │  • Load Balancing                                           │    │
│  │  • Authentication & Authorization                           │    │
│  │  • Rate Limiting                                            │    │
│  │  • Service Discovery                                        │    │
│  └────┬────────┬────────┬──────────┬────────────┬─────────────┘    │
└───────┼────────┼────────┼──────────┼────────────┼──────────────────┘
        │        │        │          │            │
        │        │        │          │            │
┌───────▼────┐ ┌▼──────┐ ┌▼────────┐ ┌▼─────────┐ ┌▼──────────┐
│   NLP      │ │ SIEM  │ │Reporting│ │Blockchain│ │   LLM     │
│  Service   │ │Service│ │ Service │ │ Service  │ │  Engine   │
└────────────┘ └───────┘ └─────────┘ └──────────┘ └───────────┘
```

---

## Detailed Microservices Architecture

```
┌──────────────────────────────────────────────────────────────────────┐
│                       MICROSERVICES LAYER                             │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  1. NLP Service (Port 8001)                                  │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  • Natural Language Understanding                     │   │   │
│  │  │  • Intent Recognition & Entity Extraction            │   │   │
│  │  │  • Query Parsing & Semantic Analysis                 │   │   │
│  │  │  • AI-Powered Summarization                          │   │   │
│  │  │  • Multi-language Support                            │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  Tech: FastAPI, OpenAI API, Transformers, spaCy          │   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  2. SIEM Connector Service (Port 8002)                      │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  • Elasticsearch Query Builder                        │   │   │
│  │  │  • Multi-Index Search                                 │   │   │
│  │  │  • Real-time Log Streaming                            │   │   │
│  │  │  • Data Aggregation & Filtering                       │   │   │
│  │  │  • Query Optimization                                 │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  Tech: FastAPI, Elasticsearch Client, Asyncio            │   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  3. Reporting Service (Port 8003)                           │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  • PDF Report Generation                              │   │   │
│  │  │  • Executive Summary Creation                         │   │   │
│  │  │  • Chart & Graph Generation                           │   │   │
│  │  │  • Template Management                                │   │   │
│  │  │  • Export to Multiple Formats                         │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  Tech: FastAPI, ReportLab, Jinja2, Matplotlib            │   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │  4. Blockchain Audit Service (Port 8004)                    │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │  • Immutable Audit Trail Logging                      │   │   │
│  │  │  • Transaction Hash Generation                        │   │   │
│  │  │  • Cryptographic Verification                         │   │   │
│  │  │  • Compliance Record Keeping                          │   │   │
│  │  │  • Tamper Detection                                   │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  │  Tech: FastAPI, hashlib, blockchain SDK                  │   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
```

---

## AI/ML Pipeline

```
┌──────────────────────────────────────────────────────────────────┐
│                      AI/ML PROCESSING FLOW                        │
└──────────────────────────────────────────────────────────────────┘

   User Query: "Show me failed login attempts"
        │
        ▼
   ┌────────────────────────────────────┐
   │  1. Natural Language Processing    │
   │  ────────────────────────────────  │
   │  • Tokenization                    │
   │  • Intent Classification           │
   │  • Entity Recognition (NER)        │
   │  • Sentiment Analysis              │
   └────────┬───────────────────────────┘
            │
            │ Extracted Intent: "search_logs"
            │ Entities: {"event_type": "failed_login"}
            ▼
   ┌────────────────────────────────────┐
   │  2. Query Translation              │
   │  ────────────────────────────────  │
   │  • Convert to Elasticsearch DSL    │
   │  • Add time filters                │
   │  • Apply security context          │
   │  • Optimize query performance      │
   └────────┬───────────────────────────┘
            │
            │ Generated Query: {"query": {"match": ...}}
            ▼
   ┌────────────────────────────────────┐
   │  3. Data Retrieval                 │
   │  ────────────────────────────────  │
   │  • Execute SIEM search             │
   │  • Fetch relevant logs             │
   │  • Apply result ranking            │
   │  • Extract metadata                │
   └────────┬───────────────────────────┘
            │
            │ Results: [log1, log2, log3...]
            ▼
   ┌────────────────────────────────────┐
   │  4. AI Analysis                    │
   │  ────────────────────────────────  │
   │  • Threat Severity Scoring         │
   │  • IOC Extraction                  │
   │  • Pattern Recognition             │
   │  • Anomaly Detection               │
   │  • Predictive Analytics            │
   └────────┬───────────────────────────┘
            │
            │ Analysis: {risk_score: 75, threat_level: "HIGH"}
            ▼
   ┌────────────────────────────────────┐
   │  5. Summary Generation             │
   │  ────────────────────────────────  │
   │  • LLM-based summarization         │
   │  • Timeline reconstruction         │
   │  • Relationship mapping            │
   │  • Recommendation engine           │
   └────────┬───────────────────────────┘
            │
            │ Summary: "Detected 5 failed login attempts..."
            ▼
   ┌────────────────────────────────────┐
   │  6. Response Formatting            │
   │  ────────────────────────────────  │
   │  • JSON structure creation         │
   │  • UI-ready formatting             │
   │  • Blockchain hash inclusion       │
   │  • Confidence score calculation    │
   └────────┬───────────────────────────┘
            │
            ▼
   Return to User with Rich Context
```

---

## Data Flow Diagram

```
┌─────────┐
│  USER   │
└────┬────┘
     │ 1. Natural Language Query
     ▼
┌─────────────────┐
│  API Gateway    │ ◄──┐
└────┬────────────┘    │
     │ 2. Route Query │ 8. Return Response
     ▼                 │
┌─────────────────┐    │
│  NLP Service    │    │
└────┬────────────┘    │
     │ 3. Parsed Intent│
     ▼                 │
┌─────────────────┐    │
│  SIEM Service   │    │
└────┬────────────┘    │
     │ 4. Raw Logs     │
     ▼                 │
┌─────────────────┐    │
│  NLP Service    │    │
│  (Summarize)    │    │
└────┬────────────┘    │
     │ 5. Summary      │
     ▼                 │
┌─────────────────┐    │
│ Blockchain Svc  │    │
└────┬────────────┘    │
     │ 6. Tx Hash      │
     ▼                 │
┌─────────────────┐    │
│ Reporting Svc   │    │
│ (if requested)  │    │
└────┬────────────┘    │
     │ 7. Report       │
     └─────────────────┘
```

---

## Technology Stack

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React 18         - Component-based UI framework     │   │
│  │  TailwindCSS      - Utility-first styling            │   │
│  │  JavaScript ES6+  - Modern JS features               │   │
│  │  Font Awesome     - Icons and graphics               │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                        BACKEND                                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Python 3.11+     - Core programming language        │   │
│  │  FastAPI          - Modern web framework             │   │
│  │  Uvicorn          - ASGI server                      │   │
│  │  Pydantic         - Data validation                  │   │
│  │  HTTPX            - Async HTTP client                │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      AI/ML STACK                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  OpenAI API       - LLM for NLP tasks                │   │
│  │  LangChain        - LLM orchestration (optional)     │   │
│  │  Transformers     - Pre-trained models               │   │
│  │  spaCy            - NLP pipelines                    │   │
│  │  scikit-learn     - ML utilities                     │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                      DATA LAYER                               │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Elasticsearch    - Log storage & search            │   │
│  │  Kibana           - Data visualization               │   │
│  │  Redis            - Caching (optional)               │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────┐
│                    INFRASTRUCTURE                             │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Docker           - Containerization                 │   │
│  │  Docker Compose   - Multi-container orchestration    │   │
│  │  Kubernetes       - Production orchestration         │   │
│  │  Nginx            - Reverse proxy                    │   │
│  └──────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────┘
```

---

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PRODUCTION DEPLOYMENT                     │
└─────────────────────────────────────────────────────────────┘

                    ┌──────────────┐
                    │   Internet   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Load Balancer│
                    │   (Nginx)    │
                    └──────┬───────┘
                           │
            ┌──────────────┼──────────────┐
            │              │              │
    ┌───────▼──────┐ ┌────▼─────┐ ┌─────▼──────┐
    │  Gateway-1   │ │Gateway-2 │ │ Gateway-3  │
    └───────┬──────┘ └────┬─────┘ └─────┬──────┘
            │              │              │
            └──────────────┼──────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
    ┌───▼───┐         ┌───▼───┐         ┌───▼───┐
    │  NLP  │         │ SIEM  │         │ Blockchain│
    │Cluster│         │Cluster│         │  Cluster  │
    │ 3 nodes│        │3 nodes│         │  3 nodes  │
    └───────┘         └───────┘         └───────────┘
        │                  │
        │            ┌─────▼──────┐
        │            │Elasticsearch│
        │            │  Cluster    │
        │            │  3 nodes    │
        │            └─────────────┘
        │
    ┌───▼───────┐
    │ LLM Engine│
    │  (Local)  │
    └───────────┘
```

---

## Security Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  SECURITY LAYERS                          │
└──────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────┐
│  1. Network Security Layer              │
│  • TLS/SSL Encryption                   │
│  • Firewall Rules                       │
│  • DDoS Protection                      │
│  • Rate Limiting                        │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  2. Application Security Layer          │
│  • API Authentication (JWT)             │
│  • Role-Based Access Control (RBAC)     │
│  • Input Validation & Sanitization      │
│  • CORS Configuration                   │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  3. Data Security Layer                 │
│  • Encryption at Rest                   │
│  • Encryption in Transit                │
│  • PII Data Masking                     │
│  • Secure Key Management                │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│  4. Audit & Compliance Layer            │
│  • Blockchain Audit Trail               │
│  • Comprehensive Logging                │
│  • Tamper Detection                     │
│  • Compliance Reporting                 │
└─────────────────────────────────────────┘
```

---

## Scalability Model

```
 Load Level │ Infrastructure
────────────┼─────────────────────────────────────
            │
 0-100 QPM  │ • 1 Gateway instance
 (Dev)      │ • 1 instance per microservice
            │ • Single Elasticsearch node
            │
────────────┼─────────────────────────────────────
            │
 100-1K QPM │ • 2-3 Gateway instances
 (Startup)  │ • 2 instances per microservice
            │ • 3-node Elasticsearch cluster
            │ • Redis caching layer
            │
────────────┼─────────────────────────────────────
            │
 1K-10K QPM │ • Auto-scaling Gateway (3-10)
 (Growth)   │ • Auto-scaling microservices (3-5)
            │ • 5-node Elasticsearch cluster
            │ • Redis cluster
            │ • CDN for frontend
            │
────────────┼─────────────────────────────────────
            │
 10K+ QPM   │ • Kubernetes cluster
 (Enterprise)│ • Horizontal pod autoscaling
            │ • Multi-region deployment
            │ • Elasticsearch 7+ nodes
            │ • Distributed caching
            │ • API Gateway (Kong/Apigee)
            │
```

---

## Integration Points

```
┌──────────────────────────────────────────────────────┐
│             EXTERNAL INTEGRATIONS                     │
└──────────────────────────────────────────────────────┘

ASTRA Core
    │
    ├─► SIEM Platforms
    │   ├── Splunk
    │   ├── QRadar
    │   ├── ArcSight
    │   ├── Elasticsearch/ELK
    │   └── Azure Sentinel
    │
    ├─► Threat Intelligence
    │   ├── VirusTotal API
    │   ├── AlienVault OTX
    │   ├── Threat Crowd
    │   └── MISP
    │
    ├─► Ticketing Systems
    │   ├── Jira
    │   ├── ServiceNow
    │   ├── PagerDuty
    │   └── Slack
    │
    ├─► Identity Providers
    │   ├── Active Directory
    │   ├── Okta
    │   ├── Azure AD
    │   └── LDAP
    │
    └─► Cloud Platforms
        ├── AWS CloudWatch
        ├── Azure Monitor
        ├── GCP Cloud Logging
        └── Cloud Security Posture Mgmt
```

---

## Performance Metrics

```
┌───────────────────────────────────────────────────┐
│            SYSTEM PERFORMANCE                      │
└───────────────────────────────────────────────────┘

Query Response Time:
│████████████ 95th percentile: < 500ms
│████████     90th percentile: < 300ms
│████         50th percentile: < 150ms

API Throughput:
│████████████ Peak: 10,000 requests/sec
│████████     Sustained: 5,000 requests/sec

AI Processing:
│████████████ NLP Intent Recognition: < 100ms
│████████     Summary Generation: 2-5 seconds
│████████████ IOC Extraction: < 50ms

Resource Usage (per 1000 QPM):
├─ CPU: 2-4 cores
├─ RAM: 4-8 GB
├─ Storage: 50GB + logs
└─ Network: 10Mbps avg

Availability:
│████████████ Uptime SLA: 99.9%
│████████████ Error Rate: < 0.1%
│████████████ Mean Time to Recovery: < 5 minutes
```

---

This architecture supports:
✅ Horizontal scaling
✅ High availability
✅ Fault tolerance
✅ Security best practices
✅ Easy deployment
✅ Monitoring & observability
✅ CI/CD integration
✅ Multi-cloud support
