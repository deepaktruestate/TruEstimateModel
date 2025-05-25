from flask import Flask
from truEstimate.api import property_bp, estimate_bp

app = Flask(__name__)

# Register blueprints for modular routing
app.register_blueprint(property_bp, url_prefix="/property")
app.register_blueprint(estimate_bp, url_prefix="/estimate")

# Start the Flask server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
