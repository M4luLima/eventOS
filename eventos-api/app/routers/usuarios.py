from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse
from app.core.security import get_password_hash
from app.core.deps import get_current_user, require_roles

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(usuario_in: UsuarioCreate, db: Session = Depends(get_db)):
    # RN01: Um usuário não pode utilizar o mesmo e-mail para mais de uma conta
    user_exists = db.query(Usuario).filter(Usuario.email == usuario_in.email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe uma conta cadastrada com este e-mail."
        )
    
    if usuario_in.perfil not in ["admin", "organizador", "participante"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Perfil de usuário inválido. Escolha entre admin, organizador ou participante."
        )

    novo_usuario = Usuario(
        nome=usuario_in.nome,
        email=usuario_in.email,
        senha=get_password_hash(usuario_in.senha),
        perfil=usuario_in.perfil
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return novo_usuario

@router.get("/me", response_model=UsuarioResponse)
def consultar_meus_dados(current_user: Usuario = Depends(get_current_user)):
    return current_user

@router.get("", response_model=List[UsuarioResponse], dependencies=[Depends(require_roles(["admin"]))])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuario).all()
