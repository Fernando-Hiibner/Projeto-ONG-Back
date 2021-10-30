import re
import json
from random import randint
from hashlib import sha256, md5
from flask_jwt_extended import create_access_token
from datetime import date, datetime

from ..database.conexaoMySql import ConexaoMySQL
from ..models.consultasSQL import ConsultasSQL

class LoginController:
    def createUser(self, email, password, accountType):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()
        hash = md5(str(randint(0, 1000)).encode('UTF-8')).hexdigest()
        creationDate = datetime.now()
        creationDate = creationDate.strftime("%Y-%m-%d %H:%M:%S")

        if not re.match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$',email):
            return json.dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
        else:
            try:
                sql = f"""SELECT EMAIL FROM CONTA WHERE EMAIL = '{email}';"""
                cursor.execute(sql)
                query = cursor.fetchall()

                if len(query) > 0:
                    return json.dumps({'type': 'WARNING', 'msg': 'Este email já está em uso por outro usuário!'})
                else:
                    sql = f"""INSERT INTO PROJETO_ONG.CONTA (EMAIL, SENHA, TIPO_CONTA, DATA_CRIACAO, HASH)
                              VALUES ('{email}', '{encriptedPassword}', '{accountType}', '{creationDate}', '{hash}')"""
                    cursor.execute(sql)
                    conn.commit()
                conn.close()
            except Exception as e:
                return json.dumps({'type': 'ERROR', 'msg': str(e)})
        # TODO Enviar o email com o hash pro usuario poder verificar depois
        return json.dumps({'type': 'SUCCESS', 'msg': 'Cadastro efetuado com sucesso!'})

    def authUser(hash):
        # Conectar no banco
        ...
        # Buscar os users registrados no banco

        # sql = cnxn.execute('''
        # select
        # login_usuario Login
        # ,password     psw
        # from Tabela
        # where login_usuario = '%s'
        # '''%(login))

        # for row in sql:
        #     Login = row[0]
        #     pwd = row[1]

        #     if pwd != password:
        #         return jsonify(), 401

        #     else:
        #         data = json.loads(mostraAcessoUser(login))
        #         access_token = create_access_token(identity=login)

        #         return jsonify(token=access_token,user=login, data = data), 200

    def login(email, password):
        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()

    def deleteUser(email):
        ...
        # db = DB.SQLSERVER()
        # cnxn = db.conn

        # sql = cnxn.execute('''
        # delete from Tabela
        # where login_usuario ='%s'
        # '''%(login))
        # sql.commit()

        # return json.dumps({'type': 'SUCCESS', 'msg': 'Usuário inativado com sucesso!'})

    def changePassword(email, password):
        ...
        # db = DB.SQLSERVER()
        # cnxn = db.conn

        # password = hashlib.sha256(pwd.encode('UTF-8')).hexdigest()

        # cnxn.execute('''
        #             update Tabela
        #             password = '%s'
        #             ,data_alteracao = getdate()
        #             where login_usuario = '%s'
        #             '''%(password,login))
        # cnxn.commit()

        # return json.dumps({'INFO':'Senha Alterada com Sucesso!'})