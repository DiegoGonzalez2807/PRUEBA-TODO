from flask import request
from ..modelos import db, Usuario, UsuarioSchema, Categoria, CategoriaSchema, Tarea, TareaSchema
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import get_jwt_identity, jwt_required, create_access_token
from datetime import datetime

usuario_schema = UsuarioSchema()
categoria_schema = CategoriaSchema()
tarea_schema = TareaSchema()



class VistaSignIn(Resource):
    #Funcion para revisar que el usuario se esté creando de manera correcta
    def get(self):
        return [usuario_schema.dump(usuario) for usuario in Usuario.query.all()]
    
    #Funcion definida para crear un nuevo usuario de acuerdo al JSON que envia la peticion
    #Tambien se conecta con la base de datos y hace la insercion del nuevo usuario
    def post(self):
        nuevo_usuario = Usuario(nombre_usuario=request.json["nombre_usuario"], contrasena=request.json["contrasena"])
        db.session.add(nuevo_usuario)
        db.session.commit()
        return usuario_schema.dump(nuevo_usuario)

class VistaLogIn(Resource):
    #Funcion definida para iniciar sesion con un usuario y contrasena enviadas en JSON
    #Return -> Token JWT para peticiones que necesiten permiso
    def post(self):
            u_nombre = request.json["nombre_usuario"]
            u_contrasena = request.json["contrasena"]
            usuario = Usuario.query.filter_by(nombre_usuario=u_nombre, contrasena = u_contrasena).all()
            if usuario:
                token_de_acceso = create_access_token(identity=request.json['nombre_usuario'])
                return {'token_acceso': token_de_acceso}
            else:
                return {'mensaje':'Nombre de usuario o contraseña incorrectos'}, 401

class VistaCategorias(Resource):
    #Funcion definida para enviar todas las categorias creadas
    #Return -> Lista de categorias
    def get(self):
        return [categoria_schema.dump(ca) for ca in Categoria.query.all()]
    
    #Funcion definida para crear una categoria enviando nombre y descripcion de esta
    #Return -> Categoria creada
    @jwt_required()
    def post(self):
        nueva_categoria = Categoria(nombre_categoria=request.json["nombre"], 
                                    descripcion=request.json["descripcion"])
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria)
    
    
class VistaCategoria(Resource):
    #Funcion creada para eliminar una categoria buscandola por su id
    @jwt_required()
    def delete(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        db.session.delete(categoria)
        db.session.commit()
        return 'Categoria eliminada!'
    
class VistaTareaCreate(Resource):
    #Funcion creada para retornar todas las tareas creadas en la DB
    def get(self):
        return [tarea_schema.dump(ca) for ca in Tarea.query.all()]
    
    #Funcion generada para crear una tarea enviando su texto, fecha de finalizacion e id_categoria en un JSON
    #Return -> tarea creada
    @jwt_required()
    def post(self):
        nueva_tarea = Tarea(texto_tarea=request.json["texto"], 
                            fecha_finalizacion=datetime.strptime(request.json["fecha_finalizacion"],'%Y-%m-%d %H:%M:%S')
                            )
        categoria = Categoria.query.get_or_404(request.json["id_categoria"])
        categoria.lista_tareas.append(nueva_tarea)     

        usuario = Usuario.query.filter_by(nombre_usuario=get_jwt_identity()).all()[0]
        usuario.lista_tareas.append(nueva_tarea)
        db.session.add(nueva_tarea)
        db.session.commit()
        return tarea_schema.dump(nueva_tarea)

class VistaTareas(Resource):
    #Funcion creada para retornar una tarea buscada por su ID
    #Return -> tarea buscada
    def get(self,id):
            return tarea_schema.dump(Tarea.query.get_or_404(id))
    
    #Funcion creada para actualizar una tarea buscada por ID
    @jwt_required()
    def put(self, id):
            tarea = Tarea.query.get_or_404(id)
            tarea.texto_tarea = request.json.get("texto",tarea.texto_tarea)
            tarea.fecha_finalizacion = datetime.strptime(request.json.get("fecha_finalizacion",tarea.fecha_finalizacion),'%Y-%m-%d %H:%M:%S')
            tarea.estado_tarea = request.json.get("estado_tarea",tarea.estado_tarea)
            db.session.commit()
            return tarea_schema.dump(tarea)
    
    #Funcion creada para eliminar una tarea buscada por su ID
    @jwt_required()
    def delete(self, id):
            tarea = Tarea.query.get_or_404(id)
            db.session.delete(tarea)
            db.session.commit()
            return 'Tarea eliminada!'

class VistaTareasPerUser(Resource):
     #Funcion creada para retornar todas las tareas de un usuario buscado por su nombre
     #Return -> Lista de tareas de usuario
     def get(self, usuario):
        usuario = Usuario.query.filter_by(nombre_usuario=usuario).all()[0]
        return [tarea_schema.dump(ta) for ta in usuario.lista_tareas]