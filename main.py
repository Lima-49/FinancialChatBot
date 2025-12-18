from flask import Flask
from app.api.financial_agent_endpoint import financial_agent_bp


app = Flask(__name__)
app.register_blueprint(financial_agent_bp, url_prefix="/api/v1")