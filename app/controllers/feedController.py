from json import dumps

from ..database.conexaoMySql import ConexaoMySQL
from ..models.consultasSQL import ConsultasSQL_Feed

import pandas


# TODO Isso quebra com caractere tipo ' ou " no texto
class FeedController:
    def __init__(self):
        self.consultasSql_Feed = ConsultasSQL_Feed()
        self.paginationRowCount = 10

    def postPub(self, pubInfo: dict):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        try:
            if(pubInfo['texto'] == None and pubInfo['imagem'] == None):
                conn.close()
                return dumps({'type': 'ERROR', 'msg': 'Publicação invalida!'})
            elif(len(pubInfo['texto'].strip()) <= 0 and len(pubInfo['imagem'].strip()) <= 0):
                conn.close()
                return dumps({'type': 'ERROR', 'msg': 'Publicação invalida!'})
            cursor.execute(self.consultasSql_Feed.queryInsertPub(pubInfo))
            conn.commit()
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        conn.close()
        return dumps({'type': 'SUCCESS', 'msg': 'Publicado!'})

    def loadPub(self, page: int):
        DB = ConexaoMySQL()
        conn = DB.connect()

        pageOffset = int(page)*self.paginationRowCount

        try:
            data = pandas.read_sql(self.consultasSql_Feed.queryLoadPubPage(pageOffset, self.paginationRowCount), conn)

        except Exception as e:
            conn.close()
            return dumps({})
        conn.close()
        return data.to_json(orient='records')

    def loadUserPub(self, email: str, page: int):
        DB = ConexaoMySQL()
        conn = DB.connect()

        pageOffset = int(page)*self.paginationRowCount

        try:
            data = pandas.read_sql(self.consultasSql_Feed.queryLoadUserPubPage(email, pageOffset, self.paginationRowCount), conn)

        except Exception as e:
            conn.close()
            return dumps({})
        conn.close()
        return data.to_json(orient='records')