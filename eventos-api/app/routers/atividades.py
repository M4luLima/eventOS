from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.atividade import Atividade
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.schemas.atividade import AtividadeCreate, AtividadeResponse
from app.core.deps import get_current_user, require_roles

router = APIRouter(prefix="/atividades", tags=["Atividades"])

@router.post("", response_model=AtividadeResponse, status_code=status.HTTP_201_CREATED)
def cadastrar_atividade(
    atividade_in: AtividadeCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin", "organizador"]))
):
    # RN11: Uma atividade deve estar vinculada a um evento existente
    evento = db.query(Evento).filter(Evento.id == atividade_in.evento_id).first()
    if not evento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Evento associado não foi encontrado."
        )

    if current_user.perfil == "organizador" and evento.organizador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não pode adicionar atividades a eventos de outros organizadores."
        )

    nova_atividade = Atividade(
        nome=atividade_in.nome,
        descricao=atividade_in.descricao,
        horario=atividade_in.horario,
        evento_id=atividade_in.evento_id
    )
    db.add(nova_atividade)
    db.commit()
    db.refresh(nova_atividade)
    return nova_atividade

@router.get("/evento/{evento_id}", response_model=List[AtividadeResponse])
def listar_atividades_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    return db.query(Atividade).filter(Atividade.evento_id == evento_id).all()
