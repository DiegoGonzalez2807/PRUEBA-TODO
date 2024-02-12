from flaskr import create_app
from .modelos import db, Usuario
from flask_restful import Api
from .vistas import VistaSignIn,VistaLogIn, VistaCategorias, VistaCategoria, VistaTareaCreate, VistaTareas, VistaTareasPerUser
from flask_jwt_extended import JWTManager


app = create_app('default')
app_context = app.app_context()
#con esto se asegura de que sea consistente en todos los modulos
app_context.push()

#inicializacion de la base de datos con la aplicacion como parametro
db.init_app(app)
#crear todas las tablas que se hayan definido como clases
db.create_all()

#API REST
api = Api(app)
api.add_resource(VistaSignIn, '/usuarios')
api.add_resource(VistaLogIn, '/usuarios/iniciar-sesion')
api.add_resource(VistaCategorias, '/categorias')
api.add_resource(VistaCategoria, '/categorias/<int:id_categoria>')
api.add_resource(VistaTareaCreate, '/tareas')
api.add_resource(VistaTareas, '/tareas/<int:id>')
api.add_resource(VistaTareasPerUser, '/tareas/<string:usuario>')




jwt = JWTManager(app)
