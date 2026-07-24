from fastapi import FastAPI

app = FastAPI(
    title="ExpenseTrackerAI API",
    description="Backend API for ExpenseTrackerAI",
    version="1.0.0"
)

@app.get("/")
def root():
    return {
        "message": "ExpenseTrackerAI API is running!"
    }