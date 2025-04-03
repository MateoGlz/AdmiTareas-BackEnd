from utils.db import db
from uuid import uuid4
from utils.db import db

class Prioridad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prioridad_id = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    def __init__(self,json):
            self.prioridad_id = json['prioridad_id']
            self.nombre = json['nombre']
    
class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado_id = db.Column(db.Integer)
    nombre = db.Column(db.String(50))
    def __init__(self,json):
           self.estado_id = json['estado_id']
           self.nombre = json['nombre']

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    prioridad_id = db.Column(db.Integer)
    estado_id = db.Column(db.Integer)
    fecha_creacion = db.Column(db.Date)
    fecha_vencimiento = db.Column(db.Date)
    def __init__(self,json):
           self.titulo = json['titulo']
           self.descripcion = json['descripcion']
           self.prioridad_id = json['prioridad_id']
           self.estado_id = json['estado_id']
           self.fecha_creacion = json['fecha_creacion']
           self.fecha_vencimiento = json['fecha_vencimiento']

    
