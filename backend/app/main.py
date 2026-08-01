from fastapi import FastAPI

from app.database.database import engine
from app.models.transaction import Transaction

from app.database.database import Base
from app.api.transaction import router as transaction_router 
from app.models.user import User
from app.api.auth import router as auth_router
from app.api.analytics import router as analytics_router
from app.api.budget import router as budget_router
from app.api.prediction import router as prediction_router
from app.api.insight import router as insight_router
from app.api.receipt import router as receipt_router

#Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ExpenseTrackerAI API",
    version="1.0.0"
)

app.include_router(transaction_router)
app.include_router(auth_router)
app.include_router(analytics_router)
app.include_router(budget_router)
app.include_router(prediction_router)
app.include_router(insight_router)
app.include_router(receipt_router)

@app.get("/")
def root():
    return {
        "message": "ExpenseTrackerAI API is running!"
    }