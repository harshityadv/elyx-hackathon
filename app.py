from flask import Flask
from flask_cors import CORS
from models import db
from routes import main
from config import Config
from database import init_database

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize database
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(main)

    # Initialize database with sample data
    with app.app_context():
        init_database()

    return app

if __name__ == '__main__':
    app = create_app()
    print("🚀 Starting Elyx Healthcare Dashboard...")
    print("📊 Dashboard available at: http://localhost:5000")
    print("🔧 API endpoints available at: http://localhost:5000/api/")
    print("💬 To generate conversations, make a POST request to: http://localhost:5000/api/generate-conversations")
    print("\n⚠️  Make sure Ollama is running on http://localhost:11434")
    print("   To start Ollama: ollama serve")
    print("   To pull the model: ollama pull llama3.1:8b")

    app.run(debug=True, host='0.0.0.0', port=5000)
