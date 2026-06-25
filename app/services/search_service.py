from app.repositories.search_repository import SearchRepository


class SearchService:

    def __init__(self):
        self.repository = SearchRepository()

    async def search(
        self,
        client_id: int,
        q: str,
        modulo: str,
        page: int,
        limit: int
    ):

        return await self.repository.search(
            client_id=client_id,
            q=q,
            modulo=modulo,
            page=page,
            limit=limit
        )
    
    async def update(
        self,
        data
    ):
        return await self.repository.update(
            data.client_id,
            data.dict(
                exclude_none=True
            )
        )


    async def delete(
        self,
        client_id: int,
        modulo: str,
        id_rel: int
    ):
        return await self.repository.delete(
            client_id,
            modulo,
            id_rel
        )
    
    async def activate(
        self,
        data
    ):

        return await self.repository.activate(

            data.client_id,

            data.modulo,

            data.conditions

        )
    
    async def deactivate(
        self,
        data
    ):

        return await self.repository.deactivate(

            data.client_id,

            data.modulo,

            data.conditions

        )