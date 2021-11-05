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

    def querySelectHashVerificada(self, email: str):
        """Retorna o hash e o verificada da tabela CONTA, e [] se não tiver"""
        sql = f"""SELECT HASH, VERIFICADA FROM PROJETO_ONG.CONTA WHERE EMAIL = '{email}'"""
        return sql

    def queryUpdateVerificada(self, email: str):
        """Da update na tabela CONTA, muda o verificada de 0 para 1"""
        sql = f"""UPDATE PROJETO_ONG.CONTA
                  SET VERIFICADA = 1
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

    def queryUpdateSenha(self, email: str, encriptedPassword: str):
        """Da update na tabela CONTA, muda a senha"""
        sql = f"""UPDATE PROJETO_ONG.CONTA
                  SET SENHA = '{encriptedPassword}'
                  WHERE EMAIL = '{email}'"""
        return sql
