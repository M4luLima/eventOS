from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha = Column(String(255), nullable=False)
    perfil = Column(String(20), nullable=False, default="participante")

    eventos = relationship("Evento", back_populates="organizador", cascade="all, delete-orphan")
    inscricoes = relationship("Inscricao", back_populates="usuario", cascade="all, delete-orphan")
