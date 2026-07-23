from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Expense Tracker API"
    }
    
@app.get("/hello")
def hello():
    return {
        "message": "Hello Nicholas"
    }