from flask import Flask
from .routes.home import home_bp
from .routes.shop import shop_bp
from .routes.spreadsheet import spreadsheet_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = "secret-key"
    app.register_blueprint(home_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(spreadsheet_bp)
    return app
