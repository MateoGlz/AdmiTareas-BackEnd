from flask import Blueprint,request, make_response,jsonify
from modelos.prueba.prueba import Tarea
from modelos.prueba.prueba import Prioridad
from modelos.prueba.prueba import Estado
from datetime import datetime

menu = Blueprint("menu", __name__)
from utils.db import db

@menu.route("/create_tarea", methods=['POST'])
def create_tarea():
    try:
        datos = request.get_json()

        fecha_actual = datetime.now().date()

        titulo = datos.get('titulo')
        descripcion = datos.get('descripcion')
        prioridad_id = datos.get('prioridad')
        estado_id = datos.get('estado')
        fecha_vencimiento = datos.get('fecha_vencimiento')

        if not all([titulo, descripcion, prioridad_id, estado_id]):
            return jsonify({"error": "Faltan campos obligatorios en el JSON"}), 400
        if not isinstance(titulo, str) or not isinstance(descripcion, str):
            return jsonify({"error": "Campos con tipo de dato incorrecto"}), 400

        if not isinstance(prioridad_id, int) or not isinstance(estado_id, int):
            return jsonify({"error": "Campos con tipo de dato incorrecto"}), 400
        try:
            fecha_vencimiento = datetime.strptime(fecha_vencimiento, "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Campos con tipo de dato incorrecto"}), 400
        tarea_json = {
            "titulo": titulo,
            "descripcion": descripcion,
            "prioridad_id": prioridad_id,
            "estado_id": estado_id,
            "fecha_creacion": fecha_actual,
            "fecha_vencimiento": fecha_vencimiento
        }

        nueva_tarea = Tarea(tarea_json)

        db.session.add(nueva_tarea)
        db.session.commit()

        return make_response({"Message": "Tarea creada con éxito"}, 201)

    except Exception as e:
        print("Error al crear la tarea:", str(e)) 
        return jsonify({"error": str(e)}), 500

@menu.route("/get_all_tareas",methods = ['GET'])
def get_all_tareas():
    try:
        tarea_lista = db.session.query(
        Tarea.id,
        Tarea.titulo,
        Tarea.descripcion,
        Tarea.fecha_vencimiento,
            Prioridad.nombre.label('prioridad'),
            Estado.nombre.label('estado')
        ).join(Prioridad, Tarea.prioridad_id == Prioridad.prioridad_id) \
        .join(Estado, Tarea.estado_id == Estado.estado_id) \
        .all()
        tarea_json = []
        for tarea in tarea_lista:
            tarea_json.append({
                'id': tarea.id,
                'titulo': tarea.titulo,
                'descripcion': tarea.descripcion,
                'fecha_vencimiento': tarea.fecha_vencimiento,
                'prioridad': tarea.prioridad,
                'estado': tarea.estado
        })
        response = make_response(jsonify({"tareas": tarea_json}), 200)
        return response

    except Exception as e:
        return make_response(jsonify({'error': str(e)}), 500)

@menu.route("/get_tarea/<int:id>", methods=['GET'])
def get_tarea(id):
    tarea = Tarea.query.get(id)
    if not tarea:
        return jsonify({"mensaje": "Tarea no encontrada"}), 404

    return jsonify({
        "id": tarea.id,
        "titulo": tarea.titulo,
        "descripcion": tarea.descripcion,
        "prioridad_id": tarea.prioridad_id,
        "estado_id": tarea.estado_id,
        "fecha_creacion": tarea.fecha_creacion,
        "fecha_vencimiento": tarea.fecha_vencimiento
    })


@menu.route("/actualizar_tarea/<int:id>", methods=['PUT'])
def actualizar_tarea(id):
    tarea = Tarea.query.get(id)
    if not tarea:
        return jsonify({"error": "Tarea no encontrada"}), 404

    datos = request.get_json()
    if not datos:
        return jsonify({"error": "No se recibieron datos"}), 400
    if not all([tarea.titulo, tarea.descripcion, tarea.prioridad_id, tarea.estado_id]):
        return jsonify({"error": "Faltan campos obligatorios en el JSON"}), 400
    
    try:
        tarea.titulo = datos.get('titulo', tarea.titulo)
        tarea.descripcion = datos.get('descripcion', tarea.descripcion)
        tarea.prioridad_id = datos.get('prioridad_id', tarea.prioridad_id)
        tarea.estado_id = datos.get('estado_id', tarea.estado_id)
        tarea.fecha_vencimiento = datos.get('fecha_vencimiento', tarea.fecha_vencimiento)
        db.session.commit()
        return jsonify({
            "mensaje": "Tarea actualizada exitosamente",
            "tarea": {
                "id": tarea.id,
                "titulo": tarea.titulo,
                "descripcion": tarea.descripcion,
                "prioridad_id": tarea.prioridad_id,
                "estado_id": tarea.estado_id,
                "fecha_creacion": tarea.fecha_creacion,
                "fecha_vencimiento": tarea.fecha_vencimiento
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@menu.route("/eliminar_tarea/<int:id>", methods=['DELETE'])
def eliminar_tarea(id):
    try:
        tarea = Tarea.query.get(id)

        if not tarea:
            return jsonify({"error": "Tarea no encontrada"}), 404

        db.session.delete(tarea)
        db.session.commit()

        return jsonify({"message": "Tarea eliminada exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar la tarea: {str(e)}")
        return jsonify({"error": str(e)}), 500
