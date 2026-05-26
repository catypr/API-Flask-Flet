from flask import Flask
from flask_cors import CORS
from blueprints import filmes_bp, swagger_bp
from blueprints.swagger import swagger_ui_blueprint

def create_app() -> Flask:
    app = Flask(__name__)
    
    app.config['JSON_SORT_KEYS'] = False
    app.config['CORS_ORIGINS'] = ['http://localhost:8000', 'http://127.0.0.1:8000']
    
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    app.register_blueprint(filmes_bp)
    app.register_blueprint(swagger_bp)
    app.register_blueprint(swagger_ui_blueprint, url_prefix='/swagger')
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)