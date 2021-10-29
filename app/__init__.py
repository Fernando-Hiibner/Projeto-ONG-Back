from flask import Flask
from flask_cors import CORS
import flask_monitoringdashboard as dashboard

App = Flask(__name__)
Cors = CORS(App)

dashboard.bind(App)

import app.routes