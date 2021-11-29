from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import flask_monitoringdashboard as dashboard

from pathlib import Path
from os.path import join

# UPLOAD_FOLDER = Path(join(Path(__file__).resolve().parents[2], "projeto_ong_files"))

App = Flask(__name__)
Cors = CORS(App)
Jwt = JWTManager(App)

dashboard.bind(App)

# App.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import app.routes