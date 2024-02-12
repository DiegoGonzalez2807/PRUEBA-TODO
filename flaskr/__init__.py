from flask import Flask

#fabrica de aplicativo
def create_app(config_name):
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///proyecto0_diego_gonzalez.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] ='Pr0y3cT0_C3r0'
    app.config['PROPAGATE_EXCEPTIONS']= True
    return app