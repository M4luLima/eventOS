from pydantic import BaseModel, Field
from typing import Optional

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=3, description="Nome completo do usuário")
    email: str = Field(..., pattern=EMAIL_REGEX, description="Endereço de e-mail válido")
    senha: str = Field(..., min_length=6, description="Senha de acesso")
    perfil: str = Field("participante", description="Valores permitidos: admin, organizador, participante")

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    perfil: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    perfil: str
    usuario_id: int
