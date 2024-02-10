#Imports of libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from  sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate
from os import path
from datetime import timedelta
from flask_login import LoginManager

class Base(DeclarativeBase):
  pass

#database variabel declaration
db = SQLAlchemy(model_class=Base)

#Change this to access other datbases
DB_NAME = "developer.db"

migrate = Migrate()

def create_app():
    app = Flask(__name__)

    #Configs
    app.config['SECRET_KEY'] = 'BLEAH'
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=10080)

    #Initialize db flask link
    db.init_app(app)

    #Blueprints
    from .view import view
    from .auth import auth
    from .service import service

    #Get Access routes from blueprints
    app.register_blueprint(view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(service, url_prefix='/')

    #Loads in tables
    from .models import Cars,Base,Service,Users

    #Checks if database is created in the ./instance folder. If not, create new database (and creates instance dir, if it doesn't exists).
    CheckForDatabase(app)

    #Initializes migrating for the app and database
    migrate = Migrate(app, db)


    #Sets Login Manager
    login_manager = LoginManager()
    
    #Sets blueprint that login_manger looks for when executing functions
    login_manager.login_view = "auth.login"

    #Initializes the login manager
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
            return Users.query.get(int(id))
    
    return app
   



def CheckForDatabase(app):
    if not path.exists("instance/" + DB_NAME):
        with app.app_context():
            db.create_all()
            print("Create database")
    else:
        with app.app_context():
            db.reflect()
        print("Database exists")