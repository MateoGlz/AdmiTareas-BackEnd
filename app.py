from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os 
from dotenv import load_dotenv
import requests
from utils.db import db
from routes.menu import menu 
from routes.prioridades import prioridades 
from routes.estado import estados 
load_dotenv()
connecionBDD = os.getenv('CADENA_DB')
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = connecionBDD
SQLAlchemy(app)
app.register_blueprint(menu)
app.register_blueprint(prioridades)
app.register_blueprint(estados)
@app.route("/ping")
def ping():
    return "ping"
