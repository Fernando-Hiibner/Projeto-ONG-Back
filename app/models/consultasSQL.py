class ConsultasSQL_Login:
    def querySelectEmail(self, email: str):
        """Retorna o email se ele tiver na tabela CONTA, e [] se não tiver"""
        sql = f"""SELECT EMAIL FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}';"""
        return sql

    def queryInsertConta(self, email: str, encriptedPassword: str, accountType: str, creationDate: str, hash: str):
        """Insere uma nova conta na tabela CONTA, verificada é omitido porque na tabela por padrão ja vem 0"""
        sql = f"""INSERT INTO PROJETO_ONG.CONTA (EMAIL, SENHA, TIPO_CONTA, DATA_CRIACAO, HASH)
            VALUES ('{email}', '{encriptedPassword}', '{accountType}', '{creationDate}', '{hash}')"""
        return sql

    def queryInsertVoluntario(self, email: str, name: str, surname: str, age: str, gender: str):
        """Insere um voluntario na tabela VOLUNTARIO, descricao e rank são omitidos nessa etapda"""
        sql = f"""INSERT INTO PROJETO_ONG.VOLUNTARIOS (EMAIL, NOME, SOBRENOME, IDADE, GENERO)
                  VALUES ('{email}', '{name}', '{surname}', '{age}', '{gender}')"""
        return sql

    def queryInsertOng(self, email: str, name: str):
        """Insere uma ong na tabela ONGS, descricao e descricao_doacao são omitidos nessa etapda"""
        sql = f"""INSERT INTO PROJETO_ONG.ONGS (EMAIL, NOME)
                  VALUES ('{email}', '{name}')"""
        return sql


    def querySelectHashVerificada(self, email: str):
        """Retorna o hash e o verificada da tabela CONTA, e [] se não tiver"""
        sql = f"""SELECT HASH, VERIFICADA FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}'"""
        return sql

    def queryUpdateVerificada(self, email: str, updateDate: str):
        """Da update na tabela CONTA, muda o verificada de 0 para 1"""
        sql = f"""UPDATE PROJETO_ONG.CONTA
                  SET VERIFICADA = 1
                     ,DATA_ATUALIZACAO = '{updateDate}'
                  WHERE EMAIL = '{email}'"""
        return sql

    def querySelectEmailSenhaVerificada(self, email: str):
        """Retorna o email a senha e o verificada da tabela CONTA, e [] se não tiver"""
        sql = f"""SELECT EMAIL, SENHA, VERIFICADA FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}'"""
        return sql

    def querySelectRequestMudarSenha(self, email: str):
        """Retorna o email da tabela REQUESTS_MUDAR_SENHA, e [] se não tiver"""
        sql = f"""SELECT EMAIL FROM PROJETO_ONG.REQUESTS_MUDAR_SENHA WHERE EMAIL = '{email}'"""
        return sql

    def queryInsertRequestMudarSenha(self, email: str, verification_cod: str):
        """Insere uma nova request de mudar de senha na tabela REQUESTS_MUDAR_SENHA"""
        sql = f"""INSERT INTO PROJETO_ONG.REQUESTS_MUDAR_SENHA (EMAIL, COD_VERIFICACAO)
                  VALUES ('{email}', '{verification_cod}')"""
        return sql

    def queryUpdateRequestMudarSenha(self, email: str, verification_cod: str):
        """Update na tabela PROJETO_ONG.REQUESTS_MUDAR_SENHA para mudar o verification cod"""
        sql = f"""UPDATE PROJETO_ONG.REQUESTS_MUDAR_SENHA
                  SET COD_VERIFICACAO = '{verification_cod}'
                  WHERE EMAIL = '{email}'"""
        return sql

    def querySelectEmailCodVerificacao(self, email: str):
        """Retorna o cod de verificação registrado na tabela"""
        sql = f"""SELECT COD_VERIFICACAO FROM PROJETO_ONG.REQUESTS_MUDAR_SENHA WHERE EMAIL = '{email}'"""
        return sql

    def queryUpdateSenha(self, email: str, encriptedPassword: str, updateDate: str):
        """Da update na tabela CONTA, muda a senha"""
        sql = f"""UPDATE PROJETO_ONG.CONTA
                  SET SENHA = '{encriptedPassword}'
                     ,DATA_ATUALIZACAO = '{updateDate}'
                  WHERE EMAIL = '{email}'"""
        return sql

class ConsultasSQL_Profile:
    def querySelectProfileInfos(self, email: str, tipoConta: str):
        """Retorna as informações daquela conta"""
        if(tipoConta == "Voluntario"):
            sql = f"""SELECT CONTA.SENHA
                            ,CONTA.TIPO_CONTA
                            ,CONTA.DATA_CRIACAO
                            ,CONTA.DATA_ATUALIZACAO
                            ,CONTA.HASH
                            ,CONTA.VERIFICADA
                            ,CONTA.IMAGEM_PERFIL
                            ,CONTA.IMAGEM_BANNER
                            ,VOLUNTARIO.*
                      FROM PROJETO_ONG.CONTA AS CONTA
                      INNER JOIN PROJETO_ONG.VOLUNTARIOS AS VOLUNTARIO
                      ON CONTA.EMAIL = VOLUNTARIO.EMAIL
                      WHERE CONTA.EMAIL = '{email}'"""
            return sql
        else:
            sql = f"""SELECT CONTA.SENHA
                            ,CONTA.TIPO_CONTA
                            ,CONTA.DATA_CRIACAO
                            ,CONTA.DATA_ATUALIZACAO
                            ,CONTA.HASH
                            ,CONTA.VERIFICADA
                            ,CONTA.IMAGEM_PERFIL
                            ,CONTA.IMAGEM_BANNER
                            ,ONG.*
                      FROM PROJETO_ONG.CONTA AS CONTA
                      INNER JOIN PROJETO_ONG.ONGS AS ONG
                      ON CONTA.EMAIL = ONG.EMAIL
                      WHERE CONTA.EMAIL = '{email}'"""
            return sql
    def querySelectProfilePictureAndBanner(self, email: str):
        """Retorna as imagens de perfil e baner"""
        sql = f"""SELECT IMAGEM_PERFIL, IMAGEM_BANNER FROM PROJETO_ONG.CONTA
                  WHERE EMAIL = '{email}'"""
        return sql
    def querySelectTipoConta(self, email: str):
        """Retorna o tipo da conta"""
        sql = f"""SELECT TIPO_CONTA FROM PROJETO_ONG.CONTA
                  WHERE EMAIL = '{email}'"""
        return sql

class ConsultasSQL_Feed:
    def queryInsertPub(self, pubInfo: dict):
        """Insere uma publicacao na lista de pubs"""
        sql = f"""INSERT INTO PROJETO_ONG.PUBLICACAO(NOME, SOBRENOME, EMAIL, TEXTO, IMAGEM)
                  VALUES('{pubInfo['nome']}', '{pubInfo['sobrenome']}','{pubInfo['email']}', '{pubInfo['texto']}', '{pubInfo['imagem']}')"""
        return sql

    def queryLoadPubPage(self, pageOffset: int, paginationRowCount: int):
        """Retorna uma pagina de publicação"""
        sql = f"""SELECT PUB.NOME
                        ,PUB.SOBRENOME
                        ,PUB.TEXTO
                  	    ,PUB.IMAGEM
                        ,PUB.DATA_PUBLICACAO
                        ,CONTA.IMAGEM_BANNER
                        ,CONTA.IMAGEM_PERFIL
                   FROM PROJETO_ONG.PUBLICACAO AS PUB
                  INNER JOIN PROJETO_ONG.CONTA AS CONTA
                  ON PUB.EMAIL = CONTA.EMAIL
                  ORDER BY PUB.DATA_PUBLICACAO DESC
                  LIMIT {pageOffset},{paginationRowCount}"""
        return sql

    def queryLoadUserPubPage(self, email: str, pageOffset: int, paginationRowCount: int):
        """Retorna uma pagina de publicação de um usuario especifico"""
        sql = f"""SELECT PUB.NOME
                        ,PUB.SOBRENOME
                        ,PUB.TEXTO
                  	    ,PUB.IMAGEM
                        ,PUB.DATA_PUBLICACAO
                        ,CONTA.IMAGEM_BANNER
                        ,CONTA.IMAGEM_PERFIL
                   FROM PROJETO_ONG.PUBLICACAO AS PUB
                  INNER JOIN PROJETO_ONG.CONTA AS CONTA
                  ON PUB.EMAIL = CONTA.EMAIL
                  WHERE PUB.EMAIL = '{email}'
                  ORDER BY PUB.DATA_PUBLICACAO DESC
                  LIMIT {pageOffset},{paginationRowCount}"""
        return sql
