from fastapi import APIRouter, Query, HTTPException, Request
from app.services.search_service import SearchService
from app.repositories.search_repository import SearchRepository
from app.schemas.search_schema import (
    SearchCreateSchema,
    SearchUpdateSchema,
    SearchDeleteSchema,
    SearchStatusSchema
)

router = APIRouter()

service = SearchService()
repository = SearchRepository()


# GET /search
@router.get("/find")
async def search(
    request: Request,
    client_id: int = Query(...),
    q: str = Query(...),
    modulo: str | None = Query(default=None),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):

    reserved = {
        "q",
        "page",
        "limit",
        "modulo",
        "client_id"
    }

    filters = {}

    for key, value in request.query_params.items():
        if key not in reserved:
            filters[key] = value
   
    data = await service.search(
        client_id=client_id,
        q=q,
        modulo=modulo,
        page=page,
        limit=limit,
        filters=filters
    )

    return {
        "success": True,
        "query": q,
        "modulo": modulo,
        "filters": filters,
        "totals_by_module": data["totals_by_module"],
        "pagination": data["pagination"],
        "results": data["results"]
    }


# POST /search
@router.post("/create-search", status_code=201)
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

# PUT /search
@router.put("/update-search")
async def update_search(
    data: SearchUpdateSchema
):

    result = await service.update(
        data
    )

    return {
        "success": True,
        "message": "Registro actualizado",
        "data": result
    }
    
# DELETE /search
@router.delete("/delete-search")
async def delete_search(
    data: SearchDeleteSchema
):

    result = await service.delete(
        data.client_id,
        data.modulo,
        data.id_rel
    )

    return {
        "success": True,
        "message": "Registro eliminado",
        "data": result
    }

@router.patch("/activate-search")
async def activate_search(
    data: SearchStatusSchema
):

    result = await service.activate(
        data
    )

    return {

        "success": True,

        "message":
            "Registros activados",

        "data": result

    }

@router.patch("/deactivate-search")
async def deactivate_search(
    data: SearchStatusSchema
):

    result = await service.deactivate(
        data
    )

    return {

        "success": True,

        "message":
            "Registros desactivados",

        "data": result

    }