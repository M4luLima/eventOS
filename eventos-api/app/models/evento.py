from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    local = Column(String(100), nullable=False)
    data_inicio = Column(DateTime, nullable=False)
    data_fim = Column(DateTime, nullable=False)
    capacidade = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False, default="ativo")
    organizador_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    organizador = relationship("Usuario", back_populates="eventos")
    atividades = relationship("Atividade", back_populates="evento", cascade="all, delete-orphan")
    inscricoes = relationship("Inscricao", back_populates="evento", cascade="all, delete-orphan")
    ingressos = relationship("Ingresso", back_populates="evento", cascade="all, delete-orphan")
