from fastapi import APIRouter, Query, HTTPException

from app.services.search_service import SearchService
from app.repositories.search_repository import SearchRepository
from app.schemas.search_schema import SearchCreateSchema

router = APIRouter()

service = SearchService()
repository = SearchRepository()


# GET /search
@router.get("/find")
async def search(
    client_id: int = Query(...),
    q: str = Query(...),
    modulo: str | None = Query(default=None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
   
    data = await service.search(
        client_id=client_id,
        q=q,
        modulo=modulo,
        page=page,
        limit=limit
    )

    return {
        "success": True,
        "query": q,
        "modulo": modulo,
        "totals_by_module": data["totals_by_module"],
        "pagination": data["pagination"],
        "results": data["results"]
    }


# POST /search
@router.post("/find", status_code=201)
async def create_search(data: SearchCreateSchema):
    try:
        result = await repository.create(
             data.dict()
        )

        return {
            "success": True,
            "message": "Registro creado correctamente",
            "data": result
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.get("/debug-env")
async def debug_env():
    return {
        "DB1_HOST": os.getenv("DB1_HOST"),
        "DB1_NAME": os.getenv("DB1_NAME"),
        "DB1_USER": os.getenv("DB1_USER"),
        "MYSQL_USER": os.getenv("MYSQL_USER"),
    }