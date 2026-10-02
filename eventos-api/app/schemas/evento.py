from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import Optional

class EventoBase(BaseModel):
    nome: str = Field(..., min_length=1)
    descricao: Optional[str] = None
    local: str = Field(..., min_length=1)
    data_inicio: datetime
    data_fim: datetime
    capacidade: int = Field(..., gt=0, description="Capacidade máxima maior que zero")

    @field_validator("data_fim")
    @classmethod
    def validate_dates(cls, v: datetime, info):
        data_inicio = info.data.get("data_inicio")
        if data_inicio and v <= data_inicio:
            raise ValueError("A data_fim deve ser estritamente posterior à data_inicio")
        return v

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    local: Optional[str] = None
    data_inicio: Optional[datetime] = None
    data_fim: Optional[datetime] = None
    capacidade: Optional[int] = Field(None, gt=0)
    status: Optional[str] = None

class EventoResponse(EventoBase):
    id: int
    status: str
    organizador_id: int

    class Config:
        from_attributes = True
