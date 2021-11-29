from flask import request, make_response, jsonify
from flask_jwt_extended import (jwt_required)
from app import App

# Importando os controller
from .controllers.loginController import LoginController
from .controllers.feedController import FeedController
from .controllers.perfilController import PerfilController
# from .controllers.uploadController import UploadController

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

# @App.route('/uploadFile', methods=['POST'])
# def uploadFile():
#     _UploadController = UploadController
#     return _UploadController.uploadFile(request)

@App.route('/createUser', methods=['POST'])
def createUser():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.createUser(BODY['email'], BODY['password'], BODY['accountType'], BODY['userInfo'])

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

@App.route('/requestChangePassword', methods=['POST'])
def requestChangePassword():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.requestChangePassword(BODY['email'])

@App.route('/changePassword', methods=['POST'])
def changePassword():
    BODY = request.get_json(force=True)
    _LoginController = LoginController()
    return _LoginController.changePassword(BODY['email'], BODY['password'], BODY['verification_cod'])

# TODO Implementar no MVP, precisa da tela "Perfil" para funcionar
# @App.route('/deleteUser', methods=['POST'])
# def deleteUser():
#     BODY = request.get_json(force=True)
#     _LoginController = LoginController()
#     return _LoginController.deleteUser(BODY['email'])

@App.route('/getAccountType', methods=['POST'])
def getAccountType():
    BODY = request.get_json(force=True)
    _PerfilController = PerfilController()
    return _PerfilController.getAccoutType(BODY['email'])

@App.route('/profileInfos', methods=['POST'])
def profileInfos():
    BODY = request.get_json(force=True)
    _PerfilController = PerfilController()
    return _PerfilController.profileInfos(BODY['email'], BODY['tipoConta'])

@App.route('/getProfilePictureAndBanner', methods=['POST'])
def getProfilePictureAndBanner():
    BODY = request.get_json(force=True)
    _PerfilController = PerfilController()
    return _PerfilController.getProfilePictureAndBanner(BODY['email'])

@App.route('/postPub', methods=['POST'])
def postPub():
    BODY = request.get_json(force=True)
    _FeedController = FeedController()
    return _FeedController.postPub(BODY)

@App.route('/loadPub/<page>', methods=['GET'])
def loadPub(page):
    _FeedController = FeedController()
    return _FeedController.loadPub(page)

@App.route('/loadUserPub/<page>', methods=['POST'])
def loadUserPub(page):
    BODY = request.get_json(force=True)
    _FeedController = FeedController()
    return _FeedController.loadUserPub(BODY['email'], page)