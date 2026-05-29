from fastapi import FastAPI

from app.api.v1.routes.search import router as search_router

app = FastAPI()

app.include_router(
    search_router
)


@app.get("/health")
async def health():
    return {
        "status": "ok"
    }