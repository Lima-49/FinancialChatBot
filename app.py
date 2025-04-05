from flask import Flask
from Controller import clientBp
app = Flask(__name__)

app.register_blueprint(clientBp)