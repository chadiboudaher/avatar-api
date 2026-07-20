from fastapi import FastAPI, status, Depends
from fastapi.responses import JSONResponse
from routers import characters, auth, nations

from database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Avatar API")

@app.exception_handler(Exception)
async def generic_handler(request, exc):
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content={"detail": "An Unexpected error occured."})

@app.get("/")
async def root():
    return {"message": "Hello"}

app.include_router(characters.router)
app.include_router(auth.router)
app.include_router(nations.router)
