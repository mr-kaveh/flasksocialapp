import os, sys

# Adds Module Path to the Python Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask_script import Manager, Server
from application import create_app

'''
    In the application.py, the settings.py module
    is loaded and the create_app starts the application
    by Importing Views and Blueprints.
'''
app = create_app()
manager = Manager(app) # Manager takes control of the App

# Adding runserver command with server specifications
manager.add_command("runserver", Server(use_debugger=True,
                                        use_reloader=True,
                                        host=os.getenv('IP', '0.0.0.0'),
                                        port=int(os.getenv('PORT', 5000))))

if __name__ == '__main__':
    manager.run()