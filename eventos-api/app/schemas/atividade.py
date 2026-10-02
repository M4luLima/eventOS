from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AtividadeCreate(BaseModel):
    nome: str = Field(..., min_length=1)
    descricao: Optional[str] = None
    horario: datetime
    evento_id: int

class AtividadeResponse(BaseModel):
    id: int
    nome: str
    descricao: Optional[str]
    horario: datetime
    evento_id: int

    class Config:
        from_attributes = True
