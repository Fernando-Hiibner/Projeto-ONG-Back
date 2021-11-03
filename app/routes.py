from flask import request, make_response, jsonify
from flask_jwt_extended import (jwt_required)
from app import App

# Importando os controller
from .controllers.loginController import LoginController

# Bloquear logs de endpoints de rotas especificas
from werkzeug import serving
import re

parent_log_request = serving.WSGIRequestHandler.log_request


def disable_endpoint_logs():
    """Bloquear logs de endpoints de rotas especificas"""

    disabled_endpoints = ()

    parent_log_request = serving.WSGIRequestHandler.log_request

    def log_request(self, *args, **kwargs):
        if not any(re.match(f"{de}$", self.path) for de in disabled_endpoints):
            parent_log_request(self, *args, **kwargs)

    serving.WSGIRequestHandler.log_request = log_request

# Atualmente desnecessario
# disable_endpoint_logs()

@App.route('/', methods=['GET', 'POST'])
def raiz():
    return make_response(jsonify({"Mensagem" : "Bem vindo a API do Projeto ONG"})), 200

@App.route('/createUser', methods=['POST'])
def createUser():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.createUser(BODY['email'], BODY['password'], BODY['accountType'])

@App.route('/authUser', methods=['POST'])
def authUser():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.authUser(BODY['email'], BODY['hash'])

@App.route('/login', methods=['POST'])
def login():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.login(BODY['email'], BODY['password'])

@App.route('/changePassword', methods=['POST'])
def changePassword():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.changePassword(BODY['email'], BODY['password'])

@App.route('/deleteUser', methods=['POST'])
def deleteUser():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.deleteUser(BODY['email'])