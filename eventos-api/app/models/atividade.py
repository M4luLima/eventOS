from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Atividade(Base):
    __tablename__ = "atividades"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    descricao = Column(Text, nullable=True)
    horario = Column(DateTime, nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    evento = relationship("Evento", back_populates="atividades")
