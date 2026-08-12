# 📝 Task Management CRUD API

A lightweight RESTful To-Do API built with Python and FastAPI as part of the FlyRank Internship Track (Week 2). It performs full CRUD operations on an in-memory task list and provides auto-generated OpenAPI documentation via Swagger UI.

---

## 🚀 Quickstart & Setup

Follow these steps to run the API locally in under 2 minutes:

### 1. Clone the repository
```bash
git clone [https://github.com/](https://github.com/)syedabdullah1567/FlyRank-AI-Backend-Engineering-Internship.git
cd FlyRank-AI-Backend-Engineering-Internship
```

### 2. Install dependencies and start the server
```bash
pip install -r requirements.txt && uvicorn main:app --reload --port 8000
```

### 3. Sample request and response output

Request:
```bash
curl -i -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Go to the barber"}'
```

Response:
```bash
HTTP/1.1 201 Created
date: Wed, 12 Aug 2026 12:00:00 GMT
server: uvicorn
content-length: 42
content-type: application/json

{"id": 4, "title": "Go to the barber", "done": false}
```