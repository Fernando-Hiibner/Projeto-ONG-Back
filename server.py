from dotenv import load_dotenv
import os
from app import App

if __name__ == '__main__':
    # Carrega as variáveis de ambiente
    load_dotenv()

    PORT = os.environ.get('FLASK_PORT')
    #app.run(threaded=True, host='0.0.0.0', port=int(PORT))
    App.run(host='127.0.0.1', port=int(PORT), debug = True)
