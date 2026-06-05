from math import ceil
from datetime import datetime, timezone

from app.core.database import get_collection


class SearchRepository:

    async def search(
        self,
        client_id: int,
        q: str,
        modulo: str | None,
        page: int,
        limit: int
    ):

        collection = await get_collection(client_id)

        skip = (page - 1) * limit

        # -----------------------------------
        # QUERY GLOBAL
        # -----------------------------------

        query_global = {
            "estado": "activo",
            "$text": {
                "$search": q
            }
        }

        # -----------------------------------
        # QUERY MODULO ACTUAL
        # -----------------------------------

        query_main = query_global.copy()

        if modulo:
            query_main["modulo"] = modulo

        # -----------------------------------
        # TOTAL MODULO
        # -----------------------------------

        total = await collection.count_documents(
            query_main
        )

        # -----------------------------------
        # RESULTADOS
        # -----------------------------------

        cursor = (
            collection.find(
                query_main,
                {
                    "score": {
                        "$meta": "textScore"
                    }
                }
            )
            .sort([
                ("score", {"$meta": "textScore"})
            ])
            .skip(skip)
            .limit(limit)
        )

        results = await cursor.to_list(length=limit)

        # -----------------------------------
        # AGRUPACION POR MODULO
        # -----------------------------------

        pipeline = [
            {
                "$match": query_global
            },
            {
                "$group": {
                    "_id": "$modulo",
                    "total": {
                        "$sum": 1
                    }
                }
            }
        ]

        module_totals_raw = await (
            collection.aggregate(pipeline)
            .to_list(length=None)
        )

        totals_by_module = {}

        for item in module_totals:

            module_name = item["_id"]

            if modulo and module_name == modulo:
                continue

            totals_by_module[module_name] = item["total"]

        # -----------------------------------
        # SERIALIZACION
        # -----------------------------------

        for item in results:

            item["_id"] = str(item["_id"])

            # opcional:
            # convertir score float
            if "score" in item:
                item["score"] = float(item["score"])

        total_pages = ceil(total / limit) if total > 0 else 1

        return {

            "results": results,

            "totals_by_module": totals_by_module,

            "pagination": {
                "total": total,
                "page": page,
                "limit": limit,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
                "next_page": page + 1 if page < total_pages else None,
                "prev_page": page - 1 if page > 1 else None
            }
        }

    async def create(self, data: dict):

        collection = await get_collection(data["client_id"])

        data["fecha_actualizacion"] = datetime.now(
            timezone.utc
        )

        result = await collection.insert_one(data)

        document = await collection.find_one({
            "_id": result.inserted_id
        })

        document["_id"] = str(document["_id"])

        return document