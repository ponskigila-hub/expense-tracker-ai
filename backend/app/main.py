from contextlib import asynccontextmanager

from fastapi import FastAPI


from app.api.transaction import router as transaction_router 
from app.api.auth import router as auth_router
from app.api.analytics import router as analytics_router
from app.api.budget import router as budget_router
from app.api.prediction import router as prediction_router
from app.api.insight import router as insight_router
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

app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(budget_router)
app.include_router(prediction_router)
app.include_router(insight_router)
app.include_router(receipt_router)
app.include_router(recurring_transaction_router)
app.include_router(notification_router)
app.include_router(export_router)

@app.get("/")
def root():
    return {
        "message": "ExpenseTrackerAI API is running!"
    }