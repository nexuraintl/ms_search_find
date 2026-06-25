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

        for item in module_totals_raw:

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

        data["fecha_actualizacion"] = datetime.now(timezone.utc)

        await collection.update_one(
            {
                "modulo": data["modulo"],
                "id_rel": data["id_rel"]
            },
            {
                "$setOnInsert": data
            },
            upsert=True
        )

        document = await collection.find_one({
            "modulo": data["modulo"],
            "id_rel": data["id_rel"]
        })

        document["_id"] = str(document["_id"])

        return document

    async def update(
        self,
        client_id: int,
        data: dict
    ):

        collection = await get_collection(
            client_id
        )

        modulo = data.pop("modulo")
        id_rel = data.pop("id_rel")

        data["fecha_actualizacion"] = (
            datetime.utcnow()
        )

        result = await collection.update_one(
            {
                "modulo": modulo,
                "id_rel": id_rel
            },
            {
                "$set": data
            }
        )

        return {
            "matched_count": result.matched_count,
            "modified_count": result.modified_count
        }
    
    async def delete(
        self,
        client_id: int,
        modulo: str,
        id_rel: int
    ):

        collection = await get_collection(
            client_id
        )

        result = await collection.delete_one(
            {
                "modulo": modulo,
                "id_rel": id_rel
            }
        )

        return {
            "deleted_count": result.deleted_count
        }
    
    def build_conditions_query(
        self,
        modulo: str,
        conditions: dict
    ):

        query = {
            "modulo": modulo
        }

        metadata = conditions.get(
            "metadata",
            {}
        )

        for field, values in metadata.items():

            query[
                f"metadata.{field}"
            ] = {
                "$in": values
            }

        return query
    
    async def activate(
        self,
        client_id: int,
        modulo: str,
        conditions: dict
    ):

        collection = await get_collection(
            client_id
        )

        query = self.build_conditions_query(
            modulo,
            conditions
        )

        result = await collection.update_many(

            query,

            {
                "$set": {

                    "estado": "activo",

                    "fecha_actualizacion":
                        datetime.now(
                            timezone.utc
                        )

                }
            }

        )

        return {

            "matched": result.matched_count,

            "modified": result.modified_count

        }
    
    async def deactivate(
        self,
        client_id: int,
        modulo: str,
        conditions: dict
    ):

        collection = await get_collection(
            client_id
        )

        query = self.build_conditions_query(
            modulo,
            conditions
        )

        result = await collection.update_many(

            query,

            {
                "$set": {

                    "estado": "inactivo",

                    "fecha_actualizacion":
                        datetime.now(
                            timezone.utc
                        )

                }
            }

        )

        return {

            "matched": result.matched_count,

            "modified": result.modified_count

        }