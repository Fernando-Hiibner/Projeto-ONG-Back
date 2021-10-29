from flask import request, make_response, jsonify
from app import App

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

@App.route('/')
def raiz():
    return make_response(jsonify({"Mensagem" : "Bem vindo a API do Projeto ONG"})), 200