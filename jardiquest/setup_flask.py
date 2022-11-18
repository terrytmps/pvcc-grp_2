from datetime import timedelta

from flask import Flask, session, redirect, url_for, flash, request
from flask_login import LoginManager
from werkzeug.exceptions import HTTPException

from jardiquest import controller, model
from jardiquest.controller import handling_status_error
from jardiquest.model.database.entity.user import User
from jardiquest.setup_sql import db, database_path

# do not remove this import allows SQLAlchemy to find the table
from jardiquest.model.database.entity import accepte, annonce, catalogue, jardin, quete, recolte


# create the flask app (useful to be separate from the app.py
# to be used in the test and to put all the code in the jardiquest folder
def create_app():
    db_path = 'sqlite://' + database_path
    # config the app to make app.py the start point but the actual program is one directory lower
    flask_serv_intern = Flask(__name__,
                              static_folder="static",
                              template_folder='view')

    flask_serv_intern.config['SQLALCHEMY_DATABASE_URI'] = db_path
    flask_serv_intern.config['SECRET_KEY'] = '=xyb3y=2+z-kd!3rit)hfrg0j!e!oggyny0$5bliwlb8v76j'
    flask_serv_intern.register_blueprint(controller.app)
    flask_serv_intern.register_error_handler(HTTPException, handling_status_error)
    db.init_app(flask_serv_intern)

    with flask_serv_intern.app_context():
        db.create_all()

    # login handling
    login_manager = LoginManager()
    login_manager.login_view = 'controller.login'
    login_manager.init_app(flask_serv_intern)
    login_manager.refresh_view = 'controller.login'

    login_manager.needs_refresh_message = u"Session expirée, veuillez vous reconnecter"
    login_manager.needs_refresh_message_category = "info"

    @login_manager.unauthorized_handler
    def unauthorized_callback():
        flash("Veuillez vous connecter pour accéder à ce contenu")
        return redirect(url_for('controller.login', next=request.url))

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # all operation of closing ressources like database
    @flask_serv_intern.teardown_appcontext
    def close_ressource(exception):
        model.close_connection(exception)

    @flask_serv_intern.before_request
    def before_request():
        session.permanent = True
        flask_serv_intern.permanent_session_lifetime = timedelta(hours=4)

    return flask_serv_intern