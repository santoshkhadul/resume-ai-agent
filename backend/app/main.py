from fastapi import FastAPI

app = FastAPI(title="Resume AI Agent")


@app.get("/")
def home():
    return {"message": "Resume AI Agent is running"}