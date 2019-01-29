from flask import Flask
from flask_mongoengine import MongoEngine

db = MongoEngine()

def create_app(**config_overrides):
    '''
    Firstly, it initializes the flask app
    secondly, it loads the config file
    thirdly, it imports views and blueprints
    :return: flask app
    '''
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')

    app.config.update(config_overrides)

    db.init_app(app)

    from user.views import user_app
    app.register_blueprint(user_app)
    return app
