from sqlalchemy import Column, Integer, String, ForeignKey, JSON, create_engine
from sqlalchemy.orm import relationship, Mapped, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional, List

Base = declarative_base()

class Modelo(Base):
    __tablename__ = "modelos"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = Column(String, index=True)
    version: Mapped[str] = Column(String, index=True)
    compañia: Mapped[str] = Column(String, index=True)
    specs: Mapped[Optional[dict]] = Column(JSON, nullable=True)
    
    respuestas: Mapped[List["Respuesta"]] = relationship("Respuesta", back_populates="modelo")
    resultados: Mapped[List["Resultado"]] = relationship("Resultado", back_populates="modelo")

    def __init__(self, nombre: str, version: str, compañia: str, specs: Optional[dict]):
        self.nombre = nombre
        self.version = version
        self.compañia = compañia
        self.specs = specs

class Test(Base):
    __tablename__ = "tests"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = Column(String, index=True)
    idioma: Mapped[str] = Column(String, index=True)
    opciones: Mapped[list[str]] = Column(JSON, nullable=False)

    preguntas: Mapped[List["Pregunta"]] = relationship("Pregunta", back_populates="test")
    resultados: Mapped[List["Resultado"]] = relationship("Resultado", back_populates="test")

    def __init__(self, nombre: str, idioma: str, opciones: list[str]):
        self.nombre = nombre
        self.idioma = idioma
        self.opciones = opciones

class Pregunta(Base):
    __tablename__ = "preguntas"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    indice_pregunta: Mapped[int] = Column(Integer, index=True)
    texto: Mapped[str] = Column(String)
    idioma: Mapped[str] = Column(String, index=True)
    
    test_id: Mapped[int] = Column(Integer, ForeignKey("tests.id"))
    test: Mapped[Optional["Test"]] = relationship("Test", back_populates="preguntas")
    
    respuestas: Mapped[List["Respuesta"]] = relationship("Respuesta", back_populates="pregunta")
    resultados: Mapped[List["Resultado"]] = relationship("Resultado", back_populates="pregunta")

    def __init__(self, indice_pregunta: int, texto: str, idioma: str, test_id: int):
        self.indice_pregunta = indice_pregunta
        self.texto = texto
        self.idioma = idioma
        self.test_id = test_id

class Respuesta(Base):
    __tablename__ = "respuestas"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    respuesta_raw: Mapped[str] = Column(String)
    respuesta: Mapped[str] = Column(String)

    pregunta_id: Mapped[int] = Column(Integer, ForeignKey("preguntas.id"))
    pregunta: Mapped[Optional["Pregunta"]] = relationship("Pregunta", back_populates="respuestas")

    modelo_id: Mapped[int] = Column(Integer, ForeignKey("modelos.id"))
    modelo: Mapped[Optional["Modelo"]] = relationship("Modelo", back_populates="respuestas")

    def __init__(self, respuesta_raw: str, respuesta: str, pregunta_id: int, modelo_id: int):
        self.respuesta_raw = respuesta_raw
        self.respuesta = respuesta
        self.pregunta_id = pregunta_id
        self.modelo_id = modelo_id

class Resultado(Base):
    __tablename__ = "resultados"
    id: Mapped[int] = Column(Integer, primary_key=True, index=True)
    
    pregunta_id: Mapped[int] = Column(Integer, ForeignKey("preguntas.id"))
    pregunta: Mapped[Optional["Pregunta"]] = relationship("Pregunta", back_populates="resultados")
    
    modelo_id: Mapped[int] = Column(Integer, ForeignKey("modelos.id"))
    modelo: Mapped[Optional["Modelo"]] = relationship("Modelo", back_populates="resultados")
    
    test_id: Mapped[int] = Column(Integer, ForeignKey("tests.id"))
    test: Mapped[Optional["Test"]] = relationship("Test", back_populates="resultados")
    
    texto: Mapped[str] = Column(String)

    def __init__(self, texto: str, pregunta_id: int, modelo_id: int, test_id: int):
        self.texto = texto
        self.pregunta_id = pregunta_id
        self.modelo_id = modelo_id
        self.test_id = test_id
