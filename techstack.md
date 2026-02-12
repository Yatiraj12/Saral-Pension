# Saral Pension Assistant – Technology Stack

## 1. Core Backend

**Programming Language**

Python 3.11

**Web Framework**

FastAPI

- REST API handling
- Request validation
- JSON-based communication

**ASGI Server**

Uvicorn

**Data Validation**

Pydantic (v2)

---

## 2. AI & LLM Layer

**Large Language Model (LLM)**

Groq API

- Model: llama-3.3-70b-versatile

**LLM Usage**

- Professional advisory responses
- Structured retirement guidance
- Context-aware recommendation generation
- AI fallback controller when no official data is found

---

## 3. Retrieval-Augmented Generation (RAG)

**RAG Architecture**

- Multi-source retrieval
- Official-data-first controller
- AI fallback logic based on similarity threshold

**Data Sources**

- qa_chunks.json
- schemes_chunks.json
- retirement_chunks.json
- UPS (Unified Pension Scheme) structured JSON
- PFRDA-based official structured content

**Embeddings**

HuggingFace Embeddings

- Model: sentence-transformers/paraphrase-MiniLM-L3-v2
- Lightweight transformer optimized for deployment efficiency

**Vector Database**

FAISS (Facebook AI Similarity Search)

- Local vector storage
- Multi-index architecture:
  - qa
  - schemes
  - retirement

**Retrieval Strategy**

- similarity_search_with_score
- Score-based filtering
- Threshold controller for:
  - Official data usage
  - AI recommendation fallback

---

## 4. Prompt Engineering Layer

**Prompt Storage**

- qa_prompt.txt
- system_prompt.txt
- multilingual_prompt.txt

**Prompt Strategy**

- Advisory mode
- Structured responses
- Personalized retirement recommendations
- Official PFRDA data prioritization
- AI fallback instructions
- Professional tone enforcement

---

## 5. Controller Logic

**Retrieval Controller**

- Similarity threshold-based decision system
- If relevant chunk exists → Strict official answer
- If no relevant chunk → AI-based advisory recommendation

**Personalization Layer**

- Age-based recommendation logic
- Employment-type adaptation
- NPS eligibility-based advisory responses

---

## 6. Frontend

**Technologies**

- HTML5
- CSS3
- Vanilla JavaScript

**UI Features**

- Chat-based interface
- Single unified assistant
- Professional institutional design
- PFRDA-aligned branding approach
- Static assets served via FastAPI

---

## 7. Data Architecture

**Structured Knowledge Format**

- JSON-based chunk storage
- Section-wise structured data
- Keyword tagging
- Semantic retrieval optimization

**Content Domains Covered**

- National Pension System (NPS)
- Unified Pension Scheme (UPS)
- Tax benefits (80CCD sections)
- Contribution structure
- Investment options
- Withdrawal rules
- Family pension benefits
- Gratuity rules
- Comparative NPS vs UPS details

---

## 8. Language & Multilingual Support

**Translation Service**

language_service.py

- Optional multilingual response support
- Language parameter-based output handling

**Supported Mode**

- English (Primary)
- Extendable to regional languages

---

## 9. Project Architecture

```
FastAPI API Layer
        ↓
QA Chain
        ↓
Multi-Source Retriever
        ↓
FAISS Vector Stores
        ↓
Groq LLM (llama-3.3-70b-versatile)
        ↓
Structured Professional Response
```

**Architectural Features**

- Single unified QA chain
- Multi-source RAG retrieval
- Controller-based trust filtering
- Modular prompt system
- Clean separation of concerns
- Lightweight transformer embedding model

---

## 10. Security & Trust Model

- Official-data-first retrieval logic
- AI fallback clearly controlled
- PFRDA-aligned advisory tone
- Regulatory-safe architecture
- Deterministic system-level decision control

---

## 11. Optional Extensions (Future Ready)

- Conversation memory
- Source citations
- Confidence scoring
- Risk profile extraction
- Automated personal detail detection
- Streaming responses

---

## Summary

Saral Pension Assistant is a multi-source RAG-powered pension advisory chatbot built using:

- Python + FastAPI
- Groq LLM (llama-3.3-70b-versatile)
- FAISS vector search
- HuggingFace MiniLM embeddings
- Structured JSON knowledge base
- Controller-based official data prioritization
- Prompt-engineered advisory intelligence
- HTML/CSS/JS frontend

The system is designed to provide professional, structured, and trustworthy pension guidance aligned with PFRDA frameworks.
