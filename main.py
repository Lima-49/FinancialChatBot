from flask import Flask
from app.api.financial_agent_endpoint import financial_agent_bp
import sys
import os

#TODO: Criar uma tool que retornar buscar as compras do cartao por categoria

#TODO: Criar uma tool que busca as compras do cartao por estabelecimento
# para poder responder perguntas como "Quanto gastei no supermercado X esse mes?"

app = Flask(__name__)
app.register_blueprint(financial_agent_bp, url_prefix="/api/v1")