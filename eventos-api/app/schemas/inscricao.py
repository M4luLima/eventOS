from pydantic import BaseModel
from datetime import datetime

class InscricaoCreate(BaseModel):
    evento_id: int

class InscricaoResponse(BaseModel):
    id: int
    usuario_id: int
    evento_id: int
    data_inscricao: datetime
    status: str

    class Config:
        from_attributes = True
