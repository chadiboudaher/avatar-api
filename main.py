from fastapi import FastAPI

app = FastAPI(title="Avatar API")

@app.get("/")
async def root():
    return {
        "message": "The four nations welcome you."
    }