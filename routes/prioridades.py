from flask import Blueprint, request, make_response, Flask, jsonify
from modelos.prueba.prueba import Prioridad
from utils.db import db
from flask_cors import CORS
import traceback

prioridades = Blueprint("prioridades", __name__)

def obtener_prioridades():
    # Obtén la lista de prioridades desde la base de datos
    prioridades_lista = Prioridad.query.all()
    
    prioridades_json = []
    for prioridad in prioridades_lista:
        prioridades_json.append({
            'id': prioridad.prioridad_id,  
            'nombre': prioridad.nombre,  
        })
    response = make_response(jsonify({"Prioridades": prioridades_json}), 200)
    return response

@prioridades.route('/get_prioridades', methods=['GET'])
def get_prioridades():
    try:
        return obtener_prioridades()
    except Exception as e: 
        print(traceback.format_exc())
        return make_response({"Mensaje": str(e)}, 204)
