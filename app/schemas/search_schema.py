from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class SearchCreateSchema(BaseModel):
    modulo: str
    titulo: str
    contenido: str
    resumen: str
    tags: List[str] = []
    url: str
    estado: Optional[str] = "activo"
    fecha_actualizacion: Optional[datetime] = None
    client_id : int
    metadata: Dict[str, Any] = Field(default_factory=dict)