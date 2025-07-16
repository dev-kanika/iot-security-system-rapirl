from flask import Flask
from routes.audio_route import audio_bp
from routes.image_route import image_bp
from routes.detector_routes import detector_bp
from routes.system_routes import system_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints from each route module
    app.register_blueprint(audio_bp, url_prefix='/predict')
    app.register_blueprint(image_bp, url_prefix='/predict')
    app.register_blueprint(detector_bp, url_prefix='/detect')
    app.register_blueprint(system_bp, url_prefix='/')

    @app.route("/")
    def index():
        return "\ud83d\udd10 IoT Event Detection Backend is Live"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)