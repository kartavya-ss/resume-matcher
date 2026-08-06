from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Resume Matcher API is running"}