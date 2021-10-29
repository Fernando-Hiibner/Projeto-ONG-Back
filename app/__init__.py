from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import flask_monitoringdashboard as dashboard

App = Flask(__name__)
Cors = CORS(App)
Jwt = JWTManager(App)

dashboard.bind(App)

import app.routes