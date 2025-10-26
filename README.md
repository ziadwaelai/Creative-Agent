
# 🌟 Creative Agent – AI-Powered Marketing Content Generator

A full-stack application that generates **creative marketing campaigns** using a **6-step persona-based AI pipeline** with **real-time token streaming**.
Built with **FastAPI**, **LangChain**, **OpenAI GPT-4**, and **Streamlit**.

---

## 🚀 Core Features

| Feature                       | Description                                                                                                   |
| ----------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **6-Step Persona Pipeline**   | Product Specialist → Audience Expert → Creative Director → Content Writer → Strategy Expert → Project Manager |
| **Real-Time Token Streaming** | Watch content appear live, character-by-character, via Server-Sent Events (SSE)                               |
| **Two-Column Dashboard**      | Left: Final streaming output → Right: Step-by-step progress updates                                           |
| **Full Arabic RTL Support**   | Right-to-left interface optimized for KSA & Middle Eastern markets                                            |
| **Lightweight SSE Streaming** | Efficient HTTP-based streaming (no WebSockets)                                                                |
| **Concise Outputs**           | Each step outputs 3–4 focused markdown lines (final output: 200–250 words)                                    |
| **Strict Validation**         | Pydantic models ensure data integrity and type safety                                                         |
| **Production-Ready**          | Includes logging, error handling, and 10-minute session timeout                                               |
| **Elegant Streamlit UI**      | Clean interface with expandable sections & export options                                                     |

---

## ⚙️ Quick Start

### Prerequisites

* Python ≥ 3.9
* Valid **OpenAI API key**

### Installation

```bash
# 1️⃣ Install dependencies
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt

# 2️⃣ Add environment variables
echo "OPENAI_API_KEY=your_api_key_here" > .env

# 3️⃣ Run the backend (FastAPI + SSE)
uvicorn backend.app:app --reload

# 4️⃣ Run the frontend (Streamlit)
streamlit run frontend/app.py
```

### Access

* **Frontend:** [http://localhost:8501](http://localhost:8501)
* **API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🔌 Streaming API

### Endpoint

`POST /api/generate-creative-content-stream`
**Server-Sent Events (SSE)** endpoint for real-time AI text streaming.

#### Request

```json
{
  "client_name": "string (1–200 chars)",
  "product_description": "string (10–2000 chars)",
  "target_audience": "string (5–500 chars)",
  "tone_of_voice": ["string", "string"]
}
```

#### Streaming Response

```
event: step_start
data: {"step":1,"title":"Product Analysis"}

event: step_stream
data: {"step":1,"content":"token"}

event: step_complete
data: {"step":1,"data":"full markdown content"}
```

#### Highlights

* Token-by-token real-time streaming
* Events for all 6 persona steps
* Keeps connection alive up to 10 minutes
* Graceful disconnect and cleanup

---

## 🧠 Architecture Overview

```
Input → Validation → LangChain Pipeline (6 Steps)
|
├── Step 1: Product Analysis (3–4 lines)
├── Step 2: Audience Analysis (3–4 lines)
├── Step 3: Creative Ideas (2–3 ideas)
├── Step 4: Content Writing (80–100 words)
├── Step 5: Marketing Strategy (3–4 lines)
└── Step 6: Final Output (200–250 words)

↓
GPT-4.1 (streaming=True)
↓
Server-Sent Events → Streamlit UI (real-time update)
```

---

## 🧩 Tech Stack

| Layer          | Technology                     |
| -------------- | ------------------------------ |
| **Backend**    | FastAPI + Uvicorn              |
| **Streaming**  | Server-Sent Events (SSE)       |
| **AI Engine**  | LangChain + OpenAI GPT-4.1 |
| **Frontend**   | Streamlit                      |
| **Validation** | Pydantic                       |
| **Language**   | Python 3.9+                    |

---

## 🖥️ Frontend UI

### Dashboard Sections

| Section             | Description                                                      |
| ------------------- | ---------------------------------------------------------------- |
| **Input Form**      | Client name, product description, target audience, tone of voice |
| **Generate Button** | Starts full creative generation pipeline                         |
| **Left Column**     | Real-time streaming of final creative content                    |
| **Right Column**    | Progress view of steps 1–5 with expand/collapse                  |
| **Export Options**  | Download full markdown result with metadata                      |

### Frontend Highlights

* Full Arabic right-to-left layout
* Live progress indicators
* Expandable step previews
* Token-by-token character rendering
* Visual input validation
* Download/export ready

---

## 📁 Project Structure

```
CreativeAgent/
│
├── backend/
│   ├── app.py
│   ├── prompts/
│   ├── models/
│   └── utils/
│
├── frontend/
│   ├── app.py
│   ├── components/
│   └── assets/
│
├── .env
├── requirements.txt
└── README.md
```

---