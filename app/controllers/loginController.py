from re import match
from json import dumps
from random import randint
from datetime import datetime
from hashlib import sha256, md5
from flask_jwt_extended import create_access_token

from ..models.consultasSQL import ConsultasSQL_Login
from ..database.conexaoMySql import ConexaoMySQL
from ..config.smtpServer import Mail

class LoginController:
    def __init__(self):
        self.consultasSql_Login = ConsultasSQL_Login()
        self.accountTypes = ['Voluntario', 'ONG']

    # TODO Validar password vazio, validar accountType que não seja permitido - Pro MVP
    def createUser(self, email: str, password: str, accountType: str, userInfo: dict):
        if accountType not in self.accountTypes:
            return dumps({"type": "ERROR", "msg" : "Tipo de conta invalido!"})
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()
        hash = md5(str(randint(0, 1000)).encode('UTF-8')).hexdigest()
        creationDate = datetime.now()
        creationDate = creationDate.strftime("%Y-%m-%d %H:%M:%S")

        # TODO Isso aqui tem que ser refinado pro MVP, as validaçoes de erros, tipo email vvazio tem que ser feitas la em cima e retornar uma mensagem coerente
        try:
            if not match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
                conn.close()
                return dumps({'type': 'ERROR', 'msg': 'Email inválido!'})
            else:
                try:
                    cursor.execute(self.consultasSql_Login.querySelectEmail(email))
                    query = cursor.fetchall()

                    if len(query) > 0:
                        conn.close()
                        return dumps({'type': 'WARNING', 'msg': 'Este email já está em uso por outro usuário!'})
                    else:
                        cursor.execute(self.consultasSql_Login.queryInsertConta(email, encriptedPassword, accountType, creationDate, hash))
                        if accountType == "Voluntario":
                            # DONE Aqui inserir as informações do voluntario na tabela voluntarios
                            cursor.execute(self.consultasSql_Login.queryInsertVoluntario(email, userInfo['name'], userInfo['surname'], userInfo['age'], userInfo['gender']))
                        else:
                            # DONE Aqui inserir as informações da ong na tabela ongs
                            cursor.execute(self.consultasSql_Login.queryInsertOng(email, userInfo['name']))
                        emailSender = Mail()
                        emailSender.send([email], "Teste Projeto Ong", f"{email}\n{hash}")
                        conn.commit()
                    conn.close()
                except Exception as e:
                    conn.close()
                    return dumps({'type': 'ERROR', 'msg': str(e)})
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        return dumps({'type': 'SUCCESS', 'msg': 'Cadastro efetuado com sucesso!'})

    # DONE Atualizar a data de atualização
    def authUser(self, email: str, hash: str):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        updateDate = datetime.now()
        updateDate = updateDate.strftime("%Y-%m-%d %H:%M:%S")

        # TODO Isso aqui tem que ser refinado pro MVP, as validaçoes de erros, tipo email vvazio tem que ser feitas la em cima e retornar uma mensagem coerente
        try:
            if not match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
                conn.close()
                return dumps({'type': 'ERROR', 'msg': 'Email inválido!'})
            else:
                try:
                    cursor.execute(self.consultasSql_Login.querySelectHashVerificada(email))
                    query = cursor.fetchall()

                    if len(query) == 0:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                    dbHash = query[0][0]
                    verificada = query[0][1]

                    if verificada == 1:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Esta conta já esta verificada!'})
                    elif hash != dbHash:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Código incorreto!'})
                    elif hash == dbHash:
                        cursor.execute(self.consultasSql_Login.queryUpdateVerificada(email, updateDate))
                        conn.commit()
                    conn.close()
                except Exception as e:
                    conn.close()
                    return dumps({'type': 'ERROR', 'msg': str(e)})
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        return dumps({'type': 'SUCCESS', 'msg': 'Verificado!'})

    def login(self, email: str, password: str):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()

        # TODO Isso aqui tem que ser refinado pro MVP, as validaçoes de erros, tipo email vvazio tem que ser feitas la em cima e retornar uma mensagem coerente
        try:
            if not match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
                conn.close()
                return dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
            else:
                try:
                    cursor.execute(self.consultasSql_Login.querySelectEmailSenhaVerificada(email))
                    query = cursor.fetchall()

                    if len(query) == 0:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                    dbEmail = query[0][0]
                    dbSenha = query[0][1]
                    verificada = query[0][2]

                    # TODO Adicionar essa validação no MVP
                    # if verificada == 0:
                    #     conn.close()
                    #     return dumps({'type': 'ERROR', 'msg': 'Esta conta não esta verificada!'})
                    # elif encriptedPassword != dbSenha:
                    if encriptedPassword != dbSenha:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Senha incorreta'})
                    else:
                        accessToken = create_access_token(identity=email)
                    conn.close()
                except Exception as e:
                    conn.close()
                    return dumps({'type': 'ERROR', 'msg': str(e)})
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        return dumps({"token": accessToken, "user": email}), 200

    def deleteUser(self, email: str):
        # TODO Como pra essa primeira etapa não temos a tela de perfil finalizada, essa feature sera adiada para o MVP
        # TODO Acredito que deletando a conta ja vai deletar os dados de todas as outras tabelas em cascata
        ...

    def requestChangePassword(self, email: str):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        verification_cod = md5(str(randint(0, 1000)).encode('UTF-8')).hexdigest()

        # TODO Isso aqui tem que ser refinado pro MVP, as validaçoes de erros, tipo email vvazio tem que ser feitas la em cima e retornar uma mensagem coerente
        try:
            if not match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
                conn.close()
                return dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
            else:
                try:
                    cursor.execute(self.consultasSql_Login.querySelectEmail(email))
                    query = cursor.fetchall()

                    if len(query) == 0:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                    cursor.execute(self.consultasSql_Login.querySelectRequestMudarSenha(email))
                    query = cursor.fetchall()

                    if len(query) > 0:
                        cursor.execute(self.consultasSql_Login.queryUpdateRequestMudarSenha(email, verification_cod))
                    else:
                        cursor.execute(self.consultasSql_Login.queryInsertRequestMudarSenha(email, verification_cod))

                    emailSender = Mail()
                    emailSender.send([email], "Teste Projeto Ong", f"{verification_cod}")

                    conn.commit()
                    conn.close()
                except Exception as e:
                    conn.close()
                    return dumps({'type': 'ERROR', 'msg': str(e)})
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})

        return dumps({'type': 'SUCCESS', 'msg': 'Requisição feita com sucesso'})

    # DONE Atualizar a data de atualização
    def changePassword(self, email: str, password: str, verification_cod: str):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()
        updateDate = datetime.now()
        updateDate = updateDate.strftime("%Y-%m-%d %H:%M:%S")

        # TODO Isso aqui tem que ser refinado pro MVP, as validaçoes de erros, tipo email vvazio tem que ser feitas la em cima e retornar uma mensagem coerente
        try:
            if not match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.?([a-z]+)?$',email):
                conn.close()
                return dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
            else:
                try:
                    cursor.execute(self.consultasSql_Login.querySelectEmail(email))
                    query = cursor.fetchall()

                    if len(query) == 0:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Este email não está cadastrado!'})

                    cursor.execute(self.consultasSql_Login.querySelectEmailCodVerificacao(email))
                    query = cursor.fetchall()

                    if len(query) > 0:
                        dbVerificationCod = query[0][0]
                        if dbVerificationCod == verification_cod:
                            cursor.execute(self.consultasSql_Login.queryUpdateSenha(email, encriptedPassword, updateDate))
                            conn.commit()
                            conn.close()
                        else:
                            conn.close()
                            return dumps({'type': 'ERROR', 'msg': 'Código de verificação invalido'})

                    else:
                        conn.close()
                        return dumps({'type': 'ERROR', 'msg': 'Não há requisições para mudar de senha nesse email'})
                except Exception as e:
                    conn.close()
                    return dumps({'type': 'ERROR', 'msg': str(e)})
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})

        return dumps({'type': 'SUCCESS', 'msg': 'Cadastro efetuado com sucesso!'})