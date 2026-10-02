from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Ingresso(Base):
    __tablename__ = "ingressos"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    tipo = Column(String(50), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    quantidade = Column(Integer, nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    evento = relationship("Evento", back_populates="ingressos")
