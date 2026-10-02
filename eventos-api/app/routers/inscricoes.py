from typing import List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.inscricao import Inscricao
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.schemas.inscricao import InscricaoCreate, InscricaoResponse
from app.core.deps import get_current_user

router = APIRouter(prefix="/inscricoes", tags=["Inscrições"])

@router.post("", response_model=InscricaoResponse, status_code=status.HTTP_201_CREATED)
def realizar_inscricao(
    inscricao_in: InscricaoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    evento = db.query(Evento).filter(Evento.id == inscricao_in.evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")

    if evento.status != "ativo":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível se inscrever em um evento inativo ou cancelado."
        )

    # RN06: Um participante não pode se inscrever duas vezes no mesmo evento
    inscricao_existente = db.query(Inscricao).filter(
        Inscricao.usuario_id == current_user.id,
        Inscricao.evento_id == inscricao_in.evento_id,
        Inscricao.status == "ativa"
    ).first()
    if inscricao_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Você já possui uma inscrição ativa para este evento."
        )

    # RN07: Um evento não pode aceitar inscrições acima de sua capacidade
    total_inscritos = db.query(Inscricao).filter(
        Inscricao.evento_id == inscricao_in.evento_id,
        Inscricao.status == "ativa"
    ).count()
    if total_inscritos >= evento.capacidade:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="O evento já atingiu sua capacidade máxima de inscritos."
        )

    nova_inscricao = Inscricao(
        usuario_id=current_user.id,
        evento_id=inscricao_in.evento_id,
        data_inscricao=datetime.utcnow(),
        status="ativa"
    )
    db.add(nova_inscricao)
    db.commit()
    db.refresh(nova_inscricao)
    return nova_inscricao

@router.delete("/{inscricao_id}", status_code=status.HTTP_200_OK)
def cancelar_inscricao(
    inscricao_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    inscricao = db.query(Inscricao).filter(Inscricao.id == inscricao_id).first()
    if not inscricao:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inscrição não encontrada")

    # RN08: Um participante pode cancelar apenas sua própria inscrição (ou Admin)
    if current_user.perfil != "admin" and inscricao.usuario_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você pode cancelar apenas a sua própria inscrição."
        )

    inscricao.status = "cancelada"
    db.commit()
    return {"message": "Inscrição cancelada com sucesso.", "status": "cancelada"}

@router.get("/minhas-inscricoes", response_model=List[InscricaoResponse])
def minhas_inscricoes(
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(get_current_user)
):
    return db.query(Inscricao).filter(Inscricao.usuario_id == current_user.id).all()
