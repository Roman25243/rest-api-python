from fastapi import FastAPI
from routes import router
import uvicorn

app = FastAPI(
    title="Book Library API", description="API для бібліотеки книг", version="1.0.0"
)

app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
