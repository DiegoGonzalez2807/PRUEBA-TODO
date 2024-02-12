import datetime
import enum
from typing import Any
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields 
from sqlalchemy import UniqueConstraint
from sqlalchemy.types import DateTime

#instanciacion de base de datos
db = SQLAlchemy()

#instanciacion de hora actual
now = datetime.datetime.utcnow

class Estado(enum.Enum):
    SIN_EMPEZAR = 1
    EMPEZADA = 2
    FINALIZADA = 3

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texto_tarea = db.Column(db.String(128))
    fecha_creacion = db.Column(DateTime, default=now)
    fecha_finalizacion = db.Column(DateTime)
    estado_tarea = db.Column(db.Enum(Estado), default=Estado.SIN_EMPEZAR)
    #Creacion de llave foranea para relacion uno a muchos entre categoria y tarea
    id_categoria = db.Column(db.Integer, db.ForeignKey('categoria.id'))
    #Creacion de llave foranea para relacion uno a muchos entre usuario y tarea
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'))


#clase intermediaria para convertir una enumeracion en un diccionario para que pueda hacer la serializacion
class EnumADiccionario(fields.Field):
    #Esta es una funcion nativo de la clase, por lo que se necesita declarar self, valor, atributo, objeto y cualquier otro argumento que se requiera
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {'llave':value.name, 'valor':value.value}


class TareaSchema(SQLAlchemyAutoSchema):
    #para poder serializar el enum en el schema de tarea se llama la clase definida para hacer la serializacion del enum y que apunte al 
    # atributo estado
    estado_tarea = EnumADiccionario(attribute=('estado_tarea'))
    class Meta:
        model = Tarea
        include_relationships = True
        #la instancia se carga cuando se accede a los esquemas
        load_instance = True

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(128), unique=True)
    contrasena = db.Column(db.String(128))
    lista_tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')
    #Esta es una relacion de uno a muchos: Un usuario puede asignarse a una o varias tareas pero una o varias tareas solo pueden pertenecer a un usuario
    #lo que se hace con cascade es decir que en caso que se borre un usuario, dichas tareas que pertenezcan a el tambien van a ser eliminadas

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        include_relationships = True
        #la instancia se carga cuando se accede a los esquemas
        load_instance = True


class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(128))
    descripcion = db.Column(db.String(128))
    lista_tareas = db.relationship('Tarea', cascade='all, delete, delete-orphan')
    #Esta es una relacion de uno a muchos:Una categoría puede tener una o varias tareas pero una o varias tareas solo pueden pertenecer a una categoria
    #lo que se hace con cascade es decir que en caso que se borre una categoria , dichas tareas que pertenezcan a el tambien van a ser eliminadas

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        #la instancia se carga cuando se accede a los esquemas
        load_instance = True