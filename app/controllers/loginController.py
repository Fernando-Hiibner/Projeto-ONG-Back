import re
import json
from random import randint
from hashlib import sha256, md5
from flask_jwt_extended import create_access_token
from datetime import date, datetime

from ..database.conexaoMySql import ConexaoMySQL
from ..models.consultasSQL import ConsultasSQL
from ..config.smtpServer import Mail

class LoginController:
    def createUser(self, email, password, accountType):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()
        hash = md5(str(randint(0, 1000)).encode('UTF-8')).hexdigest()
        creationDate = datetime.now()
        creationDate = creationDate.strftime("%Y-%m-%d %H:%M:%S")

        if not re.match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
            conn.close()
            return json.dumps({'type': 'ERROR', 'msg': 'Email inválido!'})
        else:
            try:
                sql = f"""SELECT EMAIL FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}';"""
                cursor.execute(sql)
                query = cursor.fetchall()

                if len(query) > 0:
                    conn.close()
                    return json.dumps({'type': 'WARNING', 'msg': 'Este email já está em uso por outro usuário!'})
                else:
                    sql = f"""INSERT INTO PROJETO_ONG.CONTA (EMAIL, SENHA, TIPO_CONTA, DATA_CRIACAO, HASH)
                              VALUES ('{email}', '{encriptedPassword}', '{accountType}', '{creationDate}', '{hash}')"""
                    cursor.execute(sql)
                    conn.commit()
                conn.close()
            except Exception as e:
                conn.close()
                return json.dumps({'type': 'ERROR', 'msg': str(e)})
        # TODO Enviar o email com o hash pro usuario poder verificar depois
        emailSender = Mail()
        emailSender.send([email], "Teste Projeto Ong", f"{email}\n{hash}")
        return json.dumps({'type': 'SUCCESS', 'msg': 'Cadastro efetuado com sucesso!'})

    def authUser(self, email, hash):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        if not re.match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
            conn.close()
            return json.dumps({'type': 'ERROR', 'msg': 'Email inválido!'})
        else:
            try:
                sql = f"""SELECT HASH, VERIFICADA FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}'"""
                cursor.execute(sql)
                query = cursor.fetchall()

                if len(query) == 0:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                dbHash = query[0][0]
                verificada = query[0][1]

                if verificada == 1:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Esta conta já esta verificada!'})
                elif hash != dbHash:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Código incorreto!'})
                elif hash == dbHash:
                    sql = f"""UPDATE PROJETO_ONG.CONTA
                              SET VERIFICADA = 1
                              WHERE EMAIL = '{email}'"""
                    cursor.execute(sql)
                    conn.commit()
                conn.close()
            except Exception as e:
                conn.close()
                return json.dumps({'type': 'ERROR', 'msg': str(e)})
        return json.dumps({'type': 'SUCCESS', 'msg': 'Verificado!'})

    def login(self, email, password):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()

        if not re.match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
            conn.close()
            return json.dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
        else:
            try:
                sql = f"""SELECT EMAIL, SENHA, VERIFICADA FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}'"""
                cursor.execute(sql)
                query = cursor.fetchall()

                if len(query) == 0:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                dbEmail = query[0][0]
                dbSenha = query[0][1]
                verificada = query[0][2]

                if verificada == 0:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Esta conta não esta verificada!'})
                elif encriptedPassword != dbSenha:
                    conn.close()
                    return json.dumps({'type': 'ERROR', 'msg': 'Senha incorreta'})
                else:
                    accessToken = create_access_token(identity=email)
                conn.close()
            except Exception as e:
                conn.close()
                return json.dumps({'type': 'ERROR', 'msg': str(e)})
        return json.dumps({"token": accessToken, "user": email}), 200

    def deleteUser(email):
        # TODO Como pra essa primeira etapa não temos a tela de perfil finalizada, essa feature sera adiada para o MVP
        ...
        # db = DB.SQLSERVER()
        # cnxn = db.conn

        # sql = cnxn.execute('''
        # delete from Tabela
        # where login_usuario ='%s'
        # '''%(login))
        # sql.commit()

        # return json.dumps({'type': 'SUCCESS', 'msg': 'Usuário inativado com sucesso!'})

    def requestChangePassword(email):
        ...

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