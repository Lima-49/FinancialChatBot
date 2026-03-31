"""
Entry point for the application.
"""
from flask import Flask

from app.api.financial_agent_endpoint import financial_agent_bp

app = Flask(__name__)
app.register_blueprint(financial_agent_bp, url_prefix="/api/v1")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
