from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.evento import Evento
from app.models.usuario import Usuario
from app.schemas.evento import EventoCreate, EventoUpdate, EventoResponse
from app.core.deps import get_current_user, require_roles

router = APIRouter(prefix="/eventos", tags=["Eventos"])

@router.get("", response_model=List[EventoResponse])
def listar_eventos(db: Session = Depends(get_db)):
    return db.query(Evento).filter(Evento.status == "ativo").all()

@router.get("/{evento_id}", response_model=EventoResponse)
def obter_evento(evento_id: int, db: Session = Depends(get_db)):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")
    return evento

@router.post("", response_model=EventoResponse, status_code=status.HTTP_201_CREATED)
def criar_evento(
    evento_in: EventoCreate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin", "organizador"]))
):
    # RN03: Não pode cadastrar evento com data de início no passado
    now = datetime.now()
    if evento_in.data_inicio.tzinfo is not None:
        evento_in_inicio = evento_in.data_inicio.astimezone(timezone.utc).replace(tzinfo=None)
    else:
        evento_in_inicio = evento_in.data_inicio

    if evento_in_inicio < now:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é permitido cadastrar evento com data de início no passado."
        )

    # RN02 / RN05: Capacidade maior que zero e organizador vinculado
    novo_evento = Evento(
        nome=evento_in.nome,
        descricao=evento_in.descricao,
        local=evento_in.local,
        data_inicio=evento_in.data_inicio,
        data_fim=evento_in.data_fim,
        capacidade=evento_in.capacidade,
        status="ativo",
        organizador_id=current_user.id
    )
    db.add(novo_evento)
    db.commit()
    db.refresh(novo_evento)
    return novo_evento

@router.put("/{evento_id}", response_model=EventoResponse)
def editar_evento(
    evento_id: int,
    evento_in: EventoUpdate,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin", "organizador"]))
):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")

    # RN09: Organizador pode gerenciar apenas os eventos dos quais é responsável
    if current_user.perfil == "organizador" and evento.organizador_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para editar eventos de outro organizador."
        )

    for field, value in evento_in.model_dump(exclude_unset=True).items():
        setattr(evento, field, value)

    db.commit()
    db.refresh(evento)
    return evento

@router.delete("/{evento_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(
    evento_id: int,
    db: Session = Depends(get_db),
    current_user: Usuario = Depends(require_roles(["admin"]))
):
    # RN10: Apenas administradores podem excluir eventos
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Evento não encontrado")

    db.delete(evento)
    db.commit()
    return None
