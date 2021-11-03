import mysql.connector

class ConexaoMySQL:
    def __init__(self):
        self.status = "Não conectado"

    def connect(self):
        self.conn = mysql.connector.connect(
            host="localhost",
            user="developer",
            password="Baozi123"
        )
        return self.conn

if __name__ == '__main__':
    print("Por favor execute main.py")