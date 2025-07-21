from flask import Flask
from flask_cors import CORS
import os
from datetime import timedelta
import logging

def create_app():
    app = Flask(__name__)
    
    # Configure app
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    
    # Enable CORS
    CORS(app, supports_credentials=True)
    
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    
    # Register blueprints
    from app.routes import main, auth, profile
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(profile.bp)
    
    return app