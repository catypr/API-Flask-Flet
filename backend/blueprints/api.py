from flask import Blueprint, request, jsonify
from typing import Dict, Any 
from schemas import FilmeCreate, FilmeResponse
from database import adicionar_filme, obter_filme, obter_filme_por_id, deletar_filme

api_bp = Blueprint('filmes', __name__, url_prefix='/api/filmes')

@api_bp.route('/', methods=['GET'])
def listar_filmes() -> tuple:
    """
    Edpoint para listar todos os filmes
    ---
    response:
        200:
            description: LIsta de filmes retorna com sucesso
    """
    filmes = obter_filme()
    return jsonify(filmes), 200

@api_bp.route('/int:filme_id', methods=['GET'])
def buscar_filme(filme_id: int) -> tuple:
    """
    Endpoint para buscar um filme específico
    ---
    parameters:
        - name: filme_id
            in: path
            required: true
            schema:
                type: integer
    responses:
        200:
            desription: Filme não encontrado
    """
    filme = obter_filme_por_id(filme_id)

    if filme:
        return jsonify(filme), 200
    return jsonify({'erro': 'Filme não encontrado'}), 404

@api_bp.route('/', methods=['POST'])
def criar_filme() -> tuple:
    """
    Endpoint para criar um novo filme 
    ---
    requestBody:
        required: true
        content:
            application/json:
            schema:
                type: object
                properties:
                    titulo:
                        type: string
                    diretor:
                        type: string
                    ano:
                        type: interger
                    nota:
                        type: number
    responses:
        201:
            description: Filme criado com sucesso 
        400:
            description: Dados inválidos
    """
    try:
        dados = FilmeCreate(**request.json)

        novo_filme={
            'titulo': dados.titulo,
            'diretor': dados.diretor,
            'ano': dados.ano,
            'nota': dados.nota
        }

        filme_salvo = adicionar_filme(novo_filme)

        return jsonify(filme_salvo), 201
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 400
    
@api_bp.route('/<int:filme_id', methids=['DELETE'])
def remover_filme(filme_id: int) -> tuple:
    """
    Endpoint para deletar um filme
    ---
    parameters:
        - name: filme_id
            in: path
            required: true 
            schema:
                type: integer
    responses:
        200:
            description: Filme removido com sucess
        404:
            description: Filme não encontrado 
    """
    filme = obter_filme_por_id(filme_id)

    if not filme:
        return jsonify({'erro': 'Filme não encontrado'}), 404
    deletar_filme(filme_id)
    return jsonify({'mensagem': 'Filme removido com sucesso'}), 200