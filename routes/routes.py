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


@print_memory
@app.route('/', methods=['POST', 'GET'])
def start_index():
    if 'language' not in session:
        session['language'] = 'ru'
    info = ''
    if 'info' in session:
        info = session['info']
    session['info'] = ''
    return render_template("index.html", info=info)


@print_memory
@app.route('/greeting-1', methods=['POST', 'GET'])
def view_index():
    if 'language' not in session:
        session['language'] = 'ru'
    session['answered'].clear()
    if request.method == "POST":
        str_order_num = request.form['order_num']
        log.debug(f'view index. num_order: {str_order_num}')
        if re.match("[0-9]+$", str_order_num):
            # fio, iin, category, status = get_user_info(int(str_order_num))
            # log.info(f"View Index. ORDER_NUM: {int(str_order_num)}, iin: {iin}, status: {status}")
            # if status == 'Completed':
            #     return render_template("greeting-1.html", info=get_i18n_value('TEST_COMPLETED'))
            # if status == 'Stopped':
            #     return render_template("greeting-1.html", info=get_i18n_value('TEST_STOPPED'))
            # if status == 'ABSENT':
            #     return render_template("greeting-1.html", info=get_i18n_value('TEST_ABSENT'))
            # session['order_num'] = int(str_order_num)
            # session['fio'] = fio
            # session['iin'] = iin
            # session['category'] = category
            return redirect(url_for('login_page_2'))
        else:
            return render_template("greeting-1.html", info=get_i18n_value('NEED_NUM_ORDER'))
    session['fio'] = ''
    session['iin'] = ''
    session['category'] = ''
    session['order_num'] = 0
    info = ''
    if 'info' in session:
        info = session['info']
    session['info'] = ''
    logout_user()
    return render_template("greeting-1.html", info=info)
