from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    mongo.init_app(app)

    with app.app_context():
        # Importer et enregistrer les blueprints
        from .routes.user_routes import user_bp
        from .routes.agent_routes import agent_router

        app.register_blueprint(user_bp)
        app.register_blueprint(agent_router)

    return app
