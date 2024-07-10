from flask import Flask
from storage_module import Storage

def create_app():
    app = Flask(__name__)

    # Initialize storage and store in app config or extensions
    app.storage = Storage()

    # Import blueprints
    from routes.main_routes import main_bp
    from routes.bot_routes import bot_bp
    from routes.chat_routes import chat_bp

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(bot_bp, url_prefix='/bot')
    app.register_blueprint(chat_bp, url_prefix='/chat')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
