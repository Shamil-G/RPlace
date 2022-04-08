from flask import render_template, make_response
from flask_login import login_required, logout_user
from model.utils import *
from db_oracle.connect import *
# from model.send_result import send_result_arm_go, send_failed_fc_acknowledgment
from main_app import app, log
import app_config as cfg
import json
import re


status_answered = 0
if cfg.debug_level > 0:
    log.debug("Routes стартовал...")


def get_place(num_order, mask_ip):
    with get_connection().cursor() as cursor:
        place_num = cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
        status = cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
        plsql_proc(cursor, 'GET_PLACE', 'pdd.assign_place.get_place', [num_order, mask_ip, place_num, status])
        log.info(f"GET PLACE. ORDER_NUM: {num_order}, "
                 f"ip_addr: {request.remote_addr}, place_num: {place_num.getvalue()}, status: {status.getvalue()}")
        if type(status.getvalue()) is str:
            return 0, status.getvalue()
        if type(place_num.getvalue()) is str:
            return int(place_num.getvalue().split('.')[3]), ''
    return 0, 'ALL_PLACE_BUSY'


@print_memory
@app.route('/', methods=['POST', 'GET'])
def start_index():
    if 'language' not in session:
        session['language'] = 'ru'
    place_num = 0
    log.info(f"1. START INDEX. place_num: {place_num}")
    info = ''
    if request.method == "POST":
        log.info(f"2. START INDEX. place_num: {place_num}")
        str_order_num = request.form['order_num']
        ip_addr = request.remote_addr.split('.')
        mask_ip = f"{ip_addr[0]}.{ip_addr[1]}.{ip_addr[1]}."
        log.debug(f'1. START INDEX. POST. num_order: {str_order_num}, ip_addr: {ip_addr}, mask_ip: {mask_ip}')
        if re.match("[0-9]+$", str_order_num):
            place_num, status = get_place(str_order_num, mask_ip)
            log.info(f"2. START INDEX. POST. ORDER_NUM: {str_order_num}, place_num: {place_num}, status: {status}")
            if place_num > 0:
                return redirect(url_for("show_place", num_order=str_order_num, place_num=place_num))
            else:
                info = get_i18n_value(status)
                # info = get_i18n_value('ALL_PLACE_BUSY')
            log.info(f"3. START INDEX. place_num: {place_num}, info: {info}")
    log.info(f"4. START INDEX. place_num: {place_num}, info: {info}")
    return render_template("index.html", info=info, place_num=place_num)


@print_memory
@app.route('/<num_order>/<place_num>', methods=['POST', 'GET'])
def show_place(place_num, num_order):
    if 'language' not in session:
        session['language'] = 'ru'
    log.info(f"1. SHOW PLACE. num_order: {num_order}, place_num: {place_num}")
    if request.method == "POST":
        log.info(f"2. SHOW PLACE.")
        return redirect(url_for("start_index"))
    log.info(f"3. SHOW PLACE. num_order: {num_order}, place_num: {place_num}")
    return render_template("show-place.html", num_order=num_order, place_num=place_num)
