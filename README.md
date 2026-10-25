# 💰 ExpenseTrackerAI

An AI-powered personal finance management application that helps users track expenses, analyze spending habits, and receive intelligent financial insights.

Built with a modern full-stack architecture and practical machine learning for real-world expense categorization and spending analysis.

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
- 🤖 **Automatic expense categorization** — TF-IDF + Multinomial Naive Bayes classifier trained on curated Indonesian-relevant examples, with confidence scoring and keyword fallback
- 📊 **Personalized financial insights** — month-over-month and historical average comparison; optional Gemini LLM for natural-language insights
- 🧾 **Receipt OCR** — extract transaction details from receipt images (pytesseract)
- 💬 **AI Financial Assistant** — chat with your financial data using natural language
- 📉 **Spending pattern detection** — flags unusual category-level changes based on historical behavior

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
│   ├── alembic/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
├── docker-compose.yml
├── .github/workflows/
└── README.md
```

---

## 🧠 How the AI Works

### Automatic Expense Categorization
- Model: TF-IDF (1–2 grams) + Multinomial Naive Bayes
- Training data: ~100 hand-curated examples with strong Indonesian context (Gojek, Kopi Kenangan, Indomaret, PLN, Shopee, etc.)
- Confidence threshold + keyword fallback when vocabulary overlap is low
- Endpoint: `POST /predict-category`

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

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env

# Run migrations (if using Alembic)
alembic upgrade head

# Start API
uvicorn app.main:app --reload
```

API docs available at: `http://localhost:8000/docs`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up --build
```

---

## 📡 Key API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register`, `/auth/login` | Authentication |
| CRUD | `/transactions` | Transaction management |
| GET | `/dashboard`, `/summary/*` | Analytics |
| POST | `/predict-category` | AI category prediction |
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
| ML category classification | ✅ Done |
| Insights (rule-based + optional LLM) | ✅ Done |
| Receipt OCR | ✅ Done |
| AI Chat Assistant | ✅ Done |
| Docker & CI | ✅ Done |
| Advanced forecasting models | 🔜 Planned |
| Formal anomaly detection models | 🔜 Planned |
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
