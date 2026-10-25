# 💰 ExpenseTrackerAI

An AI-powered personal finance management application that helps users track expenses, analyze spending habits, and receive intelligent financial insights.

Built with a modern full-stack architecture and practical machine learning for expense categorization and spending analysis.

---

## ✨ Features

### Core Features
- User authentication (JWT-based register & login)
- Add, edit, delete, and search transactions
- Income & expense tracking with filters and pagination
- Dashboard with financial overview
- Monthly, category, and trend summaries
- Budget tracking with alerts
- Recurring transactions
- Data export
- Scheduled notifications

### AI Features
- 🤖 **Expense category prediction** — TF-IDF + Multinomial Naive Bayes classifier trained on curated Indonesian-relevant examples, with confidence scoring and keyword fallback (`POST /predict-category`)
- 📊 **Personalized financial insights** — month-over-month and historical average comparison; optional Gemini LLM for natural-language insights
- 🧾 **Receipt OCR** — extract transaction details from receipt images (pytesseract)
- 💬 **AI Financial Assistant** — chat with your financial data using natural language
- 📉 **Spending pattern detection** — flags unusual category-level changes based on historical behavior (rule-based)

---

## ⚠️ Known Limitations

Be aware of the current scope of the ML features:

| Limitation | Detail |
|------------|--------|
| **Small training set** | Category model is trained on ~100 hand-curated examples, not a large real-world transaction corpus |
| **No formal evaluation** | There is no held-out test set, cross-validation report, or published accuracy metrics yet |
| **Prediction is opt-in** | Creating a transaction does **not** auto-fill the category. The client must call `POST /predict-category` and send the predicted category if desired |
| **Unusual spending = rules, not ML** | Insights compare current vs previous month and historical averages with fixed thresholds. Formal anomaly detection models (e.g. Isolation Forest) are not implemented |
| **LLM features need a key** | Gemini-backed insights/chat only activate when `GEMINI_API_KEY` is set; otherwise the app falls back to rule-based responses |

These limits are intentional for a portfolio-stage project. The architecture is structured so the training data, classifier, and insight logic can be upgraded later without rewriting the API surface.

---

## 🏗️ Tech Stack

### Frontend
- React
- TypeScript
- Vite
- Tailwind CSS

### Backend
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic (migrations)
- APScheduler

### Database
- PostgreSQL (production)
- SQLite (development)

### AI / Machine Learning
- scikit-learn (TF-IDF + Multinomial Naive Bayes)
- pandas, NumPy
- pytesseract + Pillow (OCR)
- Optional: Google Gemini API (insights & chat enhancement)

### Auth & Security
- JWT (python-jose)
- passlib / bcrypt

### Deployment
- Docker
- GitHub Actions (CI)
- Render
- Vercel (frontend)

---

## 📂 Project Structure

```
ExpenseTrackerAI/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI routers
│   │   ├── ml/               # Category classifier, OCR, training data
│   │   ├── services/         # Business logic
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── repositories/
│   │   ├── database/
│   │   └── main.py
│   ├── alembic/              # DB migrations
│   ├── .env.example
│   ├── requirements.txt      # Backend dependencies (use this)
│   └── Dockerfile
├── frontend/
├── docker-compose.yml
├── .github/workflows/
└── README.md
```

> **Note:** A `requirements.txt` may also exist at the repo root from earlier experiments. For local backend setup, always install from **`backend/requirements.txt`**.

---

## 🧠 How the AI Works

### Expense Category Prediction
- Model: TF-IDF (1–2 grams) + Multinomial Naive Bayes
- Training data: ~100 hand-curated examples with strong Indonesian context (Gojek, Kopi Kenangan, Indomaret, PLN, Shopee, etc.)
- Confidence threshold + keyword fallback when vocabulary overlap is low
- Endpoint: `POST /predict-category`
- **Not wired into `POST /transactions` by default** — the frontend (or API client) decides whether to call prediction and pass the category

Categories include: Food, Groceries, Transportation, Entertainment, Subscription, Shopping, Bills, Health, Education, Travel, Income, and Others.

### Financial Insights
- Compares current month spending vs previous month and vs up-to-6-month category averages
- Generates rule-based insights (e.g. category up ≥15%, above historical average)
- Optionally uses Gemini for more natural language when `GEMINI_API_KEY` is set
- Endpoint: `GET /insights`

### Receipt OCR
- Upload receipt image → text extraction → structured transaction fields

### AI Chat Assistant
- Natural language queries over the user’s transaction data
- Rule-based / LLM-assisted replies depending on configuration

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) Docker

### Backend (from repo root)

```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then edit values as needed

alembic upgrade head              # apply migrations

uvicorn app.main:app --reload
```

API docs: `http://localhost:8000/docs`

Expected backend files for this flow:
- `backend/requirements.txt`
- `backend/.env.example`
- `backend/alembic/` + `backend/alembic.ini`
- `backend/app/main.py`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Docker (recommended for sharing)

From the **repo root**:

```bash
docker-compose up --build
```

Others do not need a local Python install or `pip install -r requirements.txt` when using Docker.

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register`, `/auth/login` | Authentication |
| CRUD | `/transactions` | Transaction management (category supplied by client) |
| GET | `/dashboard`, `/summary/*` | Analytics |
| POST | `/predict-category` | ML category prediction |
| GET | `/insights` | Spending insights |
| POST | `/chat` | Financial assistant |
| POST | `/receipts` | Receipt OCR upload |
| CRUD | `/budgets` | Budget management |

---

## 🗺️ Development Status

| Area | Status |
|------|--------|
| Project setup & backend foundation | ✅ Done |
| Authentication | ✅ Done |
| Transaction CRUD + search/filter | ✅ Done |
| Dashboard & analytics | ✅ Done |
| Budget & recurring transactions | ✅ Done |
| ML category classification (predict endpoint) | ✅ Done |
| Insights (rule-based + optional LLM) | ✅ Done |
| Receipt OCR | ✅ Done |
| AI Chat Assistant | ✅ Done |
| Docker & CI | ✅ Done |
| Auto-fill category on transaction create | 🔜 Not yet |
| Held-out evaluation / metrics for classifier | 🔜 Not yet |
| Advanced forecasting models | 🔜 Planned |
| Formal anomaly detection models (e.g. Isolation Forest) | 🔜 Planned |
| Goal tracking | 🔜 Planned |

---

## 🎯 Learning Objectives

This project demonstrates:
- REST API development with FastAPI
- Clean backend architecture (router → service → repository)
- Database design & migrations
- Practical machine learning integration (classical ML, not only LLM calls)
- Hybrid AI design (ML + rules + optional LLM)
- Full-stack development
- Authentication & authorization
- Docker & CI/CD basics

---

## 📄 License

This project is licensed under the MIT License.
