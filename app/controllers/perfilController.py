from json import dumps
import pandas

from ..database.conexaoMySql import ConexaoMySQL
from ..models.consultasSQL import ConsultasSQL_Profile

class PerfilController:
    def __init__(self):
        self.consultasSQL_Profile = ConsultasSQL_Profile()

    def getAccoutType(self, email: str):
        DB = ConexaoMySQL()
        conn = DB.connect()
        cursor = conn.cursor()

        try:
            cursor.execute(self.consultasSQL_Profile.querySelectTipoConta(email))
            data = cursor.fetchall()[0][0]
        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        conn.close()
        return dumps({'type': 'SUCCESS', 'data': data})

    def profileInfos(self, email: str, tipoConta: str):
        DB = ConexaoMySQL()
        conn = DB.connect()

        try:
            data = pandas.read_sql(self.consultasSQL_Profile.querySelectProfileInfos(email, tipoConta), conn)

        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        conn.close()
        return dumps({'type': 'SUCCESS', 'data': data.to_json(orient='records')})

    def getProfilePictureAndBanner(self, email: str):
        DB = ConexaoMySQL()
        conn = DB.connect()

        try:
            data = pandas.read_sql(self.consultasSQL_Profile.querySelectProfilePictureAndBanner(email), conn)

        except Exception as e:
            conn.close()
            return dumps({'type': 'ERROR', 'msg': str(e)})
        conn.close()
        return dumps({'type': 'SUCCESS', 'data': data.to_json(orient='records')})