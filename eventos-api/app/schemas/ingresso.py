from pydantic import BaseModel, Field
from typing import Optional

class IngressoCreate(BaseModel):
    tipo: str = Field(..., description="Ex: Pista, VIP, Meia-Entrada")
    preco: float = Field(..., ge=0, description="Preço do ingresso maior ou igual a zero")
    quantidade: int = Field(..., gt=0, description="Quantidade disponível maior que zero")
    evento_id: int

class IngressoResponse(BaseModel):
    id: int
    tipo: str
    preco: float
    quantidade: int
    evento_id: int

    class Config:
        from_attributes = True
