from flask import Blueprint, jsonify
from flask_swagger_ui import get_swaggerui_blueprint

swagger_bp = Blueprint('swagger', __name__)

SWAGGER_URL = '/api/docs'
API_URL = '/api/swagger.json'

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "API de Filmes",
        'dom_id': '#swagger-ui',
        'layout': 'BaseLayout',
        'deepLinking': True,
        'displayRequestDuration': True
    }
)


@swagger_bp.route('/api/swagger.json')
def swagger_spec() -> tuple:
    """Retorna a especificação OpenAPI da API"""
    return jsonify({
        "openapi": "3.0.0",
        "info": {
            "title": "API de Filmes",
            "description": "API para gerenciamento de catálogo de filmes",
            "version": "1.0.0",
            "contact": {
                "name": "Suporte da API",
                "email": "suporte@exemplo.com"
            },
            "license": {
                "name": "MIT",
                "url": "https://opensource.org/licenses/MIT"
            }
        },
        "servers": [
            {
                "url": "http://localhost:5000",
                "description": "Servidor de desenvolvimento"
            }
        ],
        "paths": {
            "/api/filmes/": {
                "get": {
                    "summary": "Lista todos os filmes",
                    "description": "Retorna uma lista completa de todos os filmes cadastrados, ordenados por nota",
                    "responses": {
                        "200": {
                            "description": "Operação bem-sucedida",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "array",
                                        "items": {
                                            "$ref": "#/components/schemas/Filme"
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "post": {
                    "summary": "Cadastra um novo filme",
                    "description": "Adiciona um novo filme ao catálogo com validação de dados",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/FilmeInput"
                                }
                            }
                        }
                    },
                    "responses": {
                        "201": {
                            "description": "Filme criado com sucesso",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Filme"
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Dados inválidos fornecidos"
                        }
                    }
                }
            },
            "/api/filmes/{id}": {
                "get": {
                    "summary": "Busca um filme por ID",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            },
                            "description": "ID do filme"
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Filme encontrado",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "$ref": "#/components/schemas/Filme"
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Filme não encontrado"
                        }
                    }
                },
                "delete": {
                    "summary": "Remove um filme",
                    "parameters": [
                        {
                            "name": "id",
                            "in": "path",
                            "required": True,
                            "schema": {
                                "type": "integer"
                            }
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Filme removido com sucesso"
                        },
                        "404": {
                            "description": "Filme não encontrado"
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Filme": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer"},
                        "titulo": {"type": "string"},
                        "diretor": {"type": "string"},
                        "ano": {"type": "integer"},
                        "nota": {"type": "number", "format": "float"},
                        "criado_em": {"type": "string", "format": "date-time"}
                    }
                },
                "FilmeInput": {
                    "type": "object",
                    "required": ["titulo", "diretor", "ano", "nota"],
                    "properties": {
                        "titulo": {"type": "string", "minLength": 1},
                        "diretor": {"type": "string", "minLength": 1},
                        "ano": {"type": "integer", "minimum": 1888, "maximum": 2026},
                        "nota": {"type": "number", "minimum": 0, "maximum": 10}
                    }
                }
            }
        }
    }), 200