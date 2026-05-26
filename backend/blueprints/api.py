from flask import Blueprint, request, jsonify
from schemas.api import FilmeCreate
from database import adicionar_filme, obter_filmes, obter_filme_por_id, deletar_filme

# Nome do blueprint alterado para 'filmes_bp' (para bater com __init__.py)
filmes_bp = Blueprint('filmes', __name__, url_prefix='/api/filmes')

@filmes_bp.route('/', methods=['GET'])
def listar_filmes():
    filmes = obter_filmes()
    return jsonify(filmes), 200

@filmes_bp.route('/<int:filme_id>', methods=['GET'])  # Corrigido
def buscar_filme(filme_id: int):
    filme = obter_filme_por_id(filme_id)
    if filme:
        return jsonify(filme), 200
    return jsonify({'erro': 'Filme não encontrado'}), 404

@filmes_bp.route('/', methods=['POST'])
def criar_filme():
    try:
        dados = FilmeCreate(**request.json)
        novo_filme = {
            'titulo': dados.titulo,
            'diretor': dados.diretor,
            'ano': dados.ano,
            'nota': dados.nota
        }
        filme_salvo = adicionar_filme(novo_filme)
        return jsonify(filme_salvo), 201
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@filmes_bp.route('/<int:filme_id>', methods=['DELETE'])  # Corrigido
def remover_filme(filme_id: int):
    filme = obter_filme_por_id(filme_id)
    if not filme:
        return jsonify({'erro': 'Filme não encontrado'}), 404
    deletar_filme(filme_id)
    return jsonify({'mensagem': 'Filme removido com sucesso'}), 200