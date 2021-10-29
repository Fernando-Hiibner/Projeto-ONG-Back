import re
import json
from hashlib import sha256
from flask_jwt_extended import create_access_token

class LoginController:
    def createUser(email, password):
        # Conecta no banco
        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()

        if not re.match(r'[a-z0-9.]+@[a-z0-9]+\.[a-z]+\.([a-z]+)?$',email):
            return json.dumps({'type': 'WARNING', 'msg': 'Email inválido!'})
        else:
            ...
        #     try:
        #         sql=cnxn.execute('''
        #         begin tran
        #             if not exists(
        #             select * from Tabela
        #             where email_usuario = '%s'
        #             )
        #             BEGIN
        #                 insert into Tabela
        #                 (colunas)
        #                 VALUES('%s', '%s','%s','%s', getdate(), getdate());
        #             END
        #             else
        #             begin
        #                 select * from Tabela
        #                 where email_usuario = '%s'
        #                 end
        #             commit tran
        #         '''%(email,nomeUser,email,login,password,email))
        #         sql.commit()

        #         rc = sql.rowcount
        #         if rc < 0:
        #             return json.dumps({'type': 'WARNING', 'msg': 'Este email já está em uso por outro usuário!'})

        #     except Exception as e:
        #         return json.dumps({'type': 'WARNING', 'msg': 'Usuário já cadastrado! '})

        # return json.dumps({'type': 'SUCCESS', 'msg': 'Cadastro efetuado com sucesso!'})

    def authUser(email, password):
        # Conectar no banco

        encriptedPassword = sha256(password.encode('UTF-8')).hexdigest()

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