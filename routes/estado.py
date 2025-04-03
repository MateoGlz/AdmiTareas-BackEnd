from flask import Blueprint, request, make_response, Flask, jsonify
from modelos.prueba.prueba import Estado
from utils.db import db
from flask_cors import CORS
import traceback

estados = Blueprint("estados", __name__)

def obtener_estados():
    # Obtén la lista de prioridades desde la base de datos
    estados_lista = Estado.query.all()
    
    estados_json = []
    for estado in estados_lista:
        estados_json.append({
            'id': estado.estado_id,  
            'nombre': estado.nombre,   
        })
    response = make_response(jsonify({"Estados": estados_json}), 200)
    return response

@estados.route('/get_estados', methods=['GET'])
def get_estados():
    try:
        return obtener_estados() 
    except Exception as e: 
        print(traceback.format_exc())
        return make_response({"Mensaje": str(e)}, 204)
