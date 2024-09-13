from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Pregunta(Base):
    __tablename__ = "preguntas"
    id = Column(Integer, primary_key=True, index=True)
    indice_pregunta = Column(Integer, index=True)  
    idioma = Column(String, index=True)
    nombre_test = Column(String, index=True)
    texto = Column(JSON, index=True) 

class Respuesta(Base):
    __tablename__ = "respuestas"
    id = Column(Integer, primary_key=True, index=True)
    indice_pregunta = Column(Integer, index=True) 
    modelo = Column(String, index=True)
    pregunta_id = Column(Integer, ForeignKey("preguntas.id"))
    respuesta = Column(String, index=True)
    pregunta = relationship("Pregunta", back_populates="respuestas")

class Resultado(Base):
    __tablename__ = "resultados"
    id = Column(Integer, primary_key=True, index=True)
    indice_pregunta = Column(Integer, index=True)  #
    modelo = Column(String, index=True)
    idioma = Column(String, index=True)
    resultado = Column(String, index=True)

Pregunta.respuestas = relationship("Respuesta", order_by=Respuesta.id, back_populates="pregunta")
