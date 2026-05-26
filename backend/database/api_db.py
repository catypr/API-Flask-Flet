from datetime import datetime
from typing import List, Dict, Optional

_api_db: List[Dict] = []
_contador_id: int = 1

def inicializar_dados() -> None:
    """Alimentar o banco com dados iniciais"""
    global _api_db, _contador_id

    filmes_iniciais = [
        {
            'id': 1,
            'titulo': 'Crepúsculo',
            'diretor': 'Catherine Hardwicke',
            'ano': 2005,
            'nota': 5.3,
            'criado_em': datetime.now()
        },
        {
            'id': 2,
            'titulo': 'A Viagem de Chihiro',
            'diretor': 'Hayao Miyazaki',
            'ano': 2001,
            'nota': 8.6,
            'criado_em': datetime.now()
        },
        {
            'id': 3,
            'titulo': 'Orgulho e Preconceito',
            'diretor': 'Joe Wright',
            'ano': 2005,
            'nota': 7.8,
            'criado_em': datetime.now()
        },
    ]

    _api_db = filmes_iniciais
    _contador_id = 4

def obter_filmes() -> List[Dict]:
    """Retornar todos os filmes ordenados por nota (decrescente)"""
    return sorted(_api_db, key=lambda x: x['nota'], reverse=True)

def obter_filme_por_id(filme_id: int) -> Optional[Dict]:
    """Busca um filme pelo ID"""
    return next((filme for filme in _api_db if filme['id'] == filme_id), None)

def adicionar_filme(filme: Dict) -> Dict:
    """Adicionar um novo filme ao banco de dados"""
    global _contador_id

    novo_filme = {
        'id': _contador_id,
        **filme,
        'criado_em': datetime.now()
    }

    _api_db.append(novo_filme)
    _contador_id

    return novo_filme

def deletar_filme(filme_id: int) -> bool:
    """Remove um filme do banco de dados"""
    global _api_db 
    quantidade_anterior = len(_api_db)
    _api_db = [filme for filme in _api_db if filme['id'] != filme_id]
    return len(_api_db) < quantidade_anterior

def obter_id() -> int:
    """Retorna o próximo ID disponível"""
    return _contador_id

inicializar_dados()