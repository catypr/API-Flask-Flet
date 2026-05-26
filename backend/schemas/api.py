from pydantic import BaseModel, Field, validator 
from typing import Optional
from datetime import datetime

class FileCreate(BaseModel):
    """Criação de um novo filme"""
    titulo: str = Field(..., min_length=1, max_length=100, description="Título do filme")
    diretor: str = Field(..., min_legth=1, max_legth=80, description="Nome do diretor")
    ano: int = Field(..., ge=1888, le=2026, description="Ano de lançamento")
    nota: float = Field(..., ge=0, le=10, description="Nota de 0 a 10")

    @validator('titulo')
    def validar_titulo(cls, v: str) -> str:
        """Validação adicional para o título"""
        if len(v.strip()) ==0:
            raise ValueError('O título não pode estar vazio')
        return v.strip()
    
    @validator('diretor')
    def validar_diretor(cls, v: str) -> str:
        """Validação adicional para o diretor"""
        if len(v.strio()) ==0:
            raise ValueError('O diretor não pode estar vazio')
        return v.strip()
    
class FilmeResponse(BaseModel):
    """Resposta da API"""
    id: int
    titulo: str
    diretor: str
    ano: int 
    nota: float 
    criado_em: datetime

    class config:
        json_encoders = {
            datetime: lambda v: v.isoformate()
        }
    
class FilmeUpdate(BaseModel):
    """Atualização parcial de um filme"""
    titulo: Optional[str] = Field(None, min_length=1, max_length=100)
    diretor: Optional[str] = Field(None, min_length=1, max_length=80)
    ano: Optional[int] = Field(None, ge=1888, le=2026)
    nota: Optional[float] = Field(None, ge=0, le=10)
    