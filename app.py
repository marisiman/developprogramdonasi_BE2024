import os
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from app.utils.db import db
from app.controllers.user import user_route
from app.controllers.program import program_route
from app.controllers.donatur import donatur_route
from app.controllers.donasi import donasi_route
from dotenv import load_dotenv
from flask_cors import CORS

# Initializing Flask application
app = Flask(__name__)

CORS(app)

load_dotenv()

# Setting database URI directly
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')

# Initializing database
db.init_app(app)

# Setting JWT secret key directly
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)

# Registering blueprints
app.register_blueprint(user_route.user_blueprint, url_prefix='/user')
app.register_blueprint(program_route.program_blueprint, url_prefix='/programs')
app.register_blueprint(donatur_route.donatur_blueprint, url_prefix='/programs/donatur')
app.register_blueprint(donasi_route.donasi_blueprint, url_prefix='/programs/donasi')

# Defining routes here
@app.route('/')
def index():
    return jsonify({'message': 'Sukses..sukses..sukess !!!'})

if __name__ == "__main__":
    if os.name == 'nt':  # Jika dijalankan di Windows
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000)
    else:  # Jika dijalankan di lingkungan Unix-like (Vercel)
        from gunicorn.app.base import Application

        class StandaloneApplication(Application):
            def __init__(self, app, options=None):
                self.application = app
                self.options = options or {}
                super().__init__()

            def load_config(self):
                config = {key: value for key, value in self.options.items()
                          if key in self.cfg.settings and value is not None}
                for key, value in config.items():
                    self.cfg.set(key.lower(), value)

            def load(self):
                return self.application

        options = {
            'bind': '%s:%s' % ('0.0.0.0', os.getenv('PORT', '5000')),
            'workers': 4,
        }
        StandaloneApplication(app, options).run()
