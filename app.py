from flask import Flask
from controller import clientBp
app = Flask(__name__)

app.register_blueprint(clientBp)