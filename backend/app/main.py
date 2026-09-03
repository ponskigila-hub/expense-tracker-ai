from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi import Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.api.transaction import router as transaction_router 
from app.api.auth import router as auth_router
from app.api.analytics import router as analytics_router
from app.api.budget import router as budget_router
from app.api.prediction import router as prediction_router
from app.api.insight import router as insight_router
from app.api.chat import router as chat_router
from app.api.receipt import router as receipt_router
from app.api.recurring_transaction import router as recurring_transaction_router
from app.api.notification import router as notification_router
from app.api.export import router as export_router
from app.scheduler import start_scheduler, shutdown_scheduler

#Base.metadata.create_all(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()


app = FastAPI(
    title="ExpenseTrackerAI API",
    version="1.0.0",
    lifespan=lifespan
)

# Allows the Vite dev server (frontend/) to call this API from the browser.
# Add your deployed frontend's origin here too once you host it somewhere.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(budget_router)
app.include_router(prediction_router)
app.include_router(insight_router)
app.include_router(chat_router)
app.include_router(receipt_router)
app.include_router(recurring_transaction_router)
app.include_router(notification_router)
app.include_router(export_router)

@app.get("/")
def root():
    return {
        "message": "ExpenseTrackerAI API is running!"
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    """
    Does a real round-trip to the database, not just a static 200 OK.
    Two reasons this matters in production: (1) it actually tells you
    whether the DB connection is healthy, not just whether the process
    is alive, and (2) Sprint 27's keep-alive ping hits this endpoint —
    querying the DB here keeps a serverless Postgres provider (e.g.
    Neon) from suspending its compute due to inactivity, in the same
    ping that keeps this web service itself from sleeping.
    """

    db.execute(text("SELECT 1"))

    return {"status": "ok"}