from flask import render_template, make_response
from flask_login import login_required, logout_user
from model.utils import *
from model.model_login import *
# from model.send_result import send_result_arm_go, send_failed_fc_acknowledgment
from main_app import app, log
from main_config import cfg
import json
import re
# from random import randrange
# from memory_profiler import profile

status_answered = 0
if cfg.debug_level > 0:
    log.debug("Routes стартовал...")


def get_place(num_order):
    # with get_connection().cursor() as cursor:
    #     place_num = cursor.var(cx_Oracle.DB_TYPE_LONG)
    #     plsql_proc(cursor, 'GET_PLACE', 'pdd.test.get_place', [num_order, place_num])
    #     log.info(f"GET PLACE. ORDER_NUM: {num_order}, ip_addr: {request.remote_addr}, place_num: {place_num.getvalue()}")
    #     return place_num.getvalue()
    return 10


@print_memory
@app.route('/', methods=['POST', 'GET'])
def start_index():
    if 'language' not in session:
        session['language'] = 'ru'
    place_num = 0
    if request.method == "POST":
        str_order_num = request.form['order_num']
        log.debug(f'view index. num_order: {str_order_num}')
        if re.match("[0-9]+$", str_order_num):
            place_num = get_place(str_order_num)
        log.info(f"ORDER_NUM: {str_order_num}, place_num: {place_num}")
    info = ''
    if 'info' in session:
        info = session['info']
    session['info'] = ''
    return render_template("index.html", info=info, place_num=place_num)

