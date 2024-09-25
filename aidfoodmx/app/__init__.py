from flask import Flask
from .routes import register_routes

def create_app():
    app = Flask(__name__)

    # Aquí puedes añadir configuraciones adicionales como la base de datos
    # app.config.from_object('config.DevelopmentConfig')

    # Registrar las rutas
    register_routes(app)

    return app
