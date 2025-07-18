from flask import Flask
from routes.audio_route import audio_bp
from routes.image_route import image_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(audio_bp)  # No prefix, so route is /audio
    app.register_blueprint(image_bp)  # No prefix, so route is /detect

    def index():
        return "IoT Event Detection Backend is Live"

    @app.route("/start_monitoring", methods=["POST"])
    def start_monitoring():
        return "abc Monitoring started"

    @app.route("/stop_monitoring", methods=["POST"])
    def stop_monitoring():
        return "Monitoring stopped"

    @app.route("/check_alerts", methods=["GET"])
    def check_alerts():
        return "No alerts"

    @app.route("/status", methods=["GET"])
    def status():
        return "System Online"

    @app.route("/heartbeat", methods=["POST"])
    def heartbeat():
        return "Heartbeat received"

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5050, debug=True)