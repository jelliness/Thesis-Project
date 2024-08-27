from flask import Flask
from app.controllers.main_controller import main_bp
from dash_app.dashboard import create_dash_app

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config.from_object('app.config.Config')

    app.register_blueprint(main_bp)

    dash_app = create_dash_app(app)

    return app, dash_app
