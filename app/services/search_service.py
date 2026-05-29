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