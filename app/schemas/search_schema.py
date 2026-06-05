from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime


class SearchCreateSchema(BaseModel):
    modulo: str
    id_rel: int
    titulo: str
    contenido: str
    resumen: str
    tags: List[str] = []
    url: str
    estado: Optional[str] = "activo"
    fecha_actualizacion: Optional[datetime] = None
    client_id : int
    metadata: Dict[str, Any] = Field(default_factory=dict)

class SearchUpdateSchema(BaseModel):
    client_id : int
    modulo: str
    id_rel: int
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    resumen: Optional[str] = None
    tags: Optional[list[str]] = None
    estado: Optional[str] = None
    url: Optional[str] = None
    metadata: Optional[dict] = None

class SearchDeleteSchema(BaseModel):
    modulo: str
    id_rel: int