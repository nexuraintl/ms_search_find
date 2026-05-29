import aiomysql

from urllib.parse import quote_plus

from motor.motor_asyncio import AsyncIOMotorClient

from app.core.mysql import get_mysql_connection


# -----------------------------------
# CACHE GLOBAL DE CLIENTES MONGO
# -----------------------------------

mongo_clients = {}


# -----------------------------------
# OBTENER CONFIG MONGO POR CLIENTE
# -----------------------------------

async def get_client_mongo_config(
    client_id: int
):

    connection = await get_mysql_connection()

    try:

        async with connection.cursor(
            aiomysql.DictCursor
        ) as cursor:

            await cursor.execute(
                """
                SELECT
                    nombreBaseDeDatos,
                    usuario,
                    contrasena,
                    hosting,
                    puerto,
                    tipoDeBaseDeDatos
                FROM tn_gestion_bdconex
                WHERE idCliente = %s
                AND tipoDeBaseDeDatos = 'MongoDB'
                LIMIT 1
                """,
                (client_id,)
            )

            result = await cursor.fetchone()

            return result

    finally:

        connection.close()


# -----------------------------------
# OBTENER COLECCION DINAMICA
# -----------------------------------

async def get_collection(client_id: int):

    config = await get_client_mongo_config(
        client_id
    )

    if not config:

        raise Exception(
            f"No existe configuración Mongo para client_id={client_id}"
        )

    # -----------------------------------
    # VALIDACION EXTRA
    # -----------------------------------

    if config["tipoDeBaseDeDatos"] != "MongoDB":

        raise Exception(
            f"Tipo de base de datos inválido para client_id={client_id}"
        )

    # -----------------------------------
    # REUTILIZAR CLIENTE MONGO
    # -----------------------------------

    if client_id not in mongo_clients:

        username = quote_plus(
            config["usuario"]
        )

        password = quote_plus(
            config["contrasena"]
        )

        mongo_uri = (
            f"mongodb://{username}:"
            f"{password}@"
            f"{config['hosting']}:"
            f"{config['puerto']}"
        )

        mongo_clients[client_id] = (
            AsyncIOMotorClient(
                mongo_uri
            )
        )

    client = mongo_clients[client_id]

    database = client[
        config["nombreBaseDeDatos"]
    ]

    return database["tn_search_data"]