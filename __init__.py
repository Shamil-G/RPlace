from flask import Flask
from model.logger import log
# from flask_cors import CORS
from flask_session import Session


app = Flask(__name__, template_folder='templates', static_folder='static')
# app.secret_key = 'this is secret key qer:ekjf;keriutype2tO287'
# cors = CORS(app, resources={r"/checkImage/*": {"origins": "*"}})
app.config.from_object('db_config.SessionConfig')
server_session = Session(app)

log.info("__INIT MAIN APP__ started")
print("__INIT MAIN APP__ started")
