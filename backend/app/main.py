from fastapi import FastAPI

from app.database.database import engine
from app.models.transaction import Transaction

from app.database.database import Base
from app.api.transaction import router as transaction_router 

#Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="ExpenseTrackerAI API",
    version="1.0.0"
)

app.include_router(transaction_router)

@app.get("/")
def root():
    return {
        "message": "ExpenseTrackerAI API is running!"
    }