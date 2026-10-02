from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.ingresso import Ingresso
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.schemas.ingresso import IngressoCreate, IngressoResponse
from app.core.deps import get_current_user, require_roles

router = APIRouter(prefix="/ingressos", tags=["Ingressos"])

@router.post("", response_model=IngressoResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_ingresso(
    ingresso_in: IngressoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin", "organizador"]))
):
    # RN12: Um ingresso deve estar vinculado a um evento existente
    evento = db.query(Evento).filter(Evento.id == ingresso_in.evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento associado não foi encontrado."
        )

    if current_user.perfil == "organizador" and evento.organizador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode cadastrar ingressos para eventos de outros organizadores."
        )

    novo_ingresso = Ingresso(
        tipo=ingresso_in.tipo,
        preco=ingresso_in.preco,
        quantidade=ingresso_in.quantidade,
        evento_id=ingresso_in.evento_id
    )
    db.add(novo_ingresso)
    db.commit()
    db.refresh(novo_ingresso)
    return novo_ingresso

@router.get("/evento/{evento_id}", response_model=List[IngressoResponse])
def listar_ingressos_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    return db.query(Ingresso).filter(Ingresso.evento_id == evento_id).all()
