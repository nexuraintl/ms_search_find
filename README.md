# Search Service

## Ejecutar

```bash
docker-compose up --build
```

## Swagger

http://localhost:8000/docs



<!--
crear el indice:
 db.tn_search_data.createIndex(
   {
      titulo: "text",
      contenido: "text",
      resumen: "text",
      tags: "text"
   },
   {
      name: "search_text_index",
      default_language: "spanish",
      weights: {
         titulo: 10,
         resumen: 5,
         tags: 3,
         contenido: 1
      }
   }
) -->
