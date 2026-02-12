🏛 Saral Pension Assistant

A professional AI-powered pension advisory chatbot built to provide structured, trustworthy, and context-aware guidance aligned with PFRDA regulations and Government of India pension frameworks.

📌 Overview

Saral Pension Assistant is a Retrieval-Augmented Generation (RAG) based intelligent pension advisory system that:

Retrieves official pension data (NPS, UPS, schemes, tax benefits)

Prioritizes PFRDA-aligned structured data

Falls back to AI-based advisory recommendations when official data is unavailable

Provides structured, professional, retirement-focused responses

Supports personalization based on user inputs

This system is designed for credibility, regulatory alignment, and financial advisory clarity.

🧠 Architecture
User Query
     ↓
FastAPI API Layer
     ↓
QA Chain (Single Unified Chain)
     ↓
Multi-Source Retriever
     ↓
FAISS Vector Stores (qa + schemes + retirement)
     ↓
Controller Logic (Official Data First)
     ↓
Groq LLM (llama-3.3-70b-versatile)
     ↓
Structured Professional Response

🚀 Key Features
1️⃣ Multi-Source RAG Retrieval

The assistant retrieves information from:

qa_chunks.json

schemes_chunks.json

retirement_chunks.json

UPS (Unified Pension Scheme) structured data

PFRDA-aligned pension knowledge

2️⃣ Official Data Controller

The system uses similarity score filtering:

If relevant official chunk exists →
Respond strictly from official PFRDA-aligned data.

If no relevant chunk exists →
Provide AI-generated professional retirement recommendation.

This ensures trust, compliance, and credibility.

3️⃣ Advisory Intelligence

The chatbot can:

Answer NPS & UPS factual queries

Explain contribution structure

Recommend suitable retirement plans

Provide tax benefit details (Section 80CCD etc.)

Compare NPS vs UPS

Suggest retirement strategies based on age

Explain withdrawal and payout structure

4️⃣ Personalized Responses

If user provides:

Age

Employment type

NPS status

The assistant:

Adapts recommendation

Suggests appropriate tier or scheme

Explains tax advantages

Provides structured retirement guidance

5️⃣ Structured Professional Output

Responses are:

Clear

Sectioned

Professional

Regulatory-safe

Institutional in tone

🏗 Technology Stack
🔹 Backend

Python 3.11

FastAPI

Uvicorn

Pydantic v2

🔹 AI & LLM

Groq API

Model: llama-3.3-70b-versatile

🔹 RAG Components

HuggingFace Embeddings

Model: sentence-transformers/paraphrase-MiniLM-L3-v2

FAISS Vector Database

Multi-index retrieval architecture

🔹 Prompt Engineering

qa_prompt.txt

system_prompt.txt

multilingual_prompt.txt

Controller-based advisory instructions

🔹 Frontend

HTML5

CSS3

Vanilla JavaScript

Static assets served via FastAPI

📂 Project Structure
saral-pension/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── logger.py
│
│   ├── api/
│   │   └── chat_routes.py
│
│   ├── chains/
│   │   └── qa_chain.py
│
│   ├── rag/
│   │   ├── loader.py
│   │   ├── embeddings.py
│   │   ├── vectorstore.py
│   │   └── retriever.py
│
│   ├── prompts/
│   │   ├── qa_prompt.txt
│   │   ├── system_prompt.txt
│   │   └── multilingual_prompt.txt
│
│   ├── services/
│   │   ├── language_service.py
│   │   └── personalization.py
│
├── static/
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
│
├── data/
│   └── nps_docs/
│
└── vectorstore/

🔍 Data Domains Covered

National Pension System (NPS)

Unified Pension Scheme (UPS)

Contribution structure

Investment patterns

Tax benefits (80CCD sections)

Assured payouts

Minimum pension rules

Withdrawal rules

Family pension

Gratuity benefits

Comparative NPS vs UPS

🛡 Trust & Compliance Design

This system is built with:

Official-data-first logic

Similarity threshold controller

Controlled AI fallback

Professional advisory tone

Clear separation of factual vs advisory output

Regulatory-aligned content handling

🌍 Multilingual Support

English (Primary)

Extendable via language service

Language parameter-based response control

🎯 System Goals

Provide reliable pension information

Align with PFRDA guidelines

Deliver structured advisory support

Avoid hallucinated financial advice

Maintain institutional credibility

Be production-ready and scalable

🔮 Future Enhancements

Source citations in responses

Confidence scoring

Conversation memory

Risk profile detection

Advanced personalization

Streaming responses

Analytics and logging

📌 Summary

Saral Pension Assistant is a unified, multi-source, RAG-powered pension advisory chatbot built with:

FastAPI

Groq LLM (llama-3.3-70b-versatile)

FAISS vector search

HuggingFace MiniLM embeddings

Structured pension knowledge base

Controller-based official data prioritization

It combines regulatory-grade knowledge with AI advisory intelligence to provide trustworthy retirement guidance.
