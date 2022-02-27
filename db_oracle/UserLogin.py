from typing import List, Any
from flask import render_template, request, redirect, flash, url_for, g, session
from flask_login import LoginManager, login_required, logout_user, login_user, current_user
import cx_Oracle
from werkzeug.security import check_password_hash, generate_password_hash
from db_oracle.connect import get_connection
from main_app import app, log
from main_config import cfg
import re


login_manager = LoginManager(app)
login_manager.login_view = 'view_index'
if cfg.debug_level > 0:
    log.debug("UserLogin стартовал...")


class User:
    id_order = int(0)
    num_order = int(0)
    active = ''
    remain_time = int(0)
    roles = ''
    ip_addr = ''
    debug = False
    msg = ''
    iin = ''
    language = ''
    list_answer = []

    def get_user_by_num_order(self, num_order, lang):
        if type(num_order) is str and not re.match("[0-9]+$", num_order):
            if 'num_order' in session:
                session['order_num'] = 0
            return
        if type(num_order) is int and int(num_order) < 1:
            return
        try:
            self.num_order = int(num_order)
            self.language = str(lang)
        except ValueError:
            session.clear()
            return
        conn = get_connection()
        cursor = conn.cursor()
        iin = cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
        id_order = cursor.var(cx_Oracle.DB_TYPE_NUMBER)
        remain_time = cursor.var(cx_Oracle.DB_TYPE_NUMBER)
        msg = cursor.var(cx_Oracle.DB_TYPE_VARCHAR)
        ip_addr = request.remote_addr
        if self.ip_addr == '':
            try:
                cursor.callproc('pdd.admin.login', (num_order, ip_addr, lang, iin, id_order, remain_time, msg))
                self.msg = msg.getvalue()
                if self.msg:
                    log.error(f"LM. ORACLE ERROR. NUM_ORDER: {num_order}, ip_addr: {request.remote_addr}, "
                              f"lang: {lang}, Error: {self.msg}")
                    print(f"--------------> msg: {msg}")
                if int(id_order.getvalue()) > 0:
                    self.iin = iin.getvalue()
                    self.id_order = int(id_order.getvalue())
                    self.remain_time = int(remain_time.getvalue())
                    self.ip_addr = request.remote_addr
            except cx_Oracle.DatabaseError as e:
                error, = e.args
                log.error(f"LM. ORACLE EXCEPTION. NUM_ORDER: {num_order}, ip_addr: {request.remote_addr}, "
                          f"lang: {lang}, Error: {error.code} : {error.message}")
            finally:
                cursor.close()
                conn.close()
        if self.id_order is None:
            log.info(f"LM. FAIL. NUM_ORDER: {num_order}, IIN: {self.iin}, ip_addr: {self.ip_addr},  "
                     f"remain_time: {self.remain_time} sec")
            return None
        else:
            if cfg.debug_level > 3:
                log.info(f"LM. SUCCESS. NUM_ORDER: {num_order}, IIN: {self.iin}, ip_addr: {self.ip_addr},  "
                         f"remain_time: {self.remain_time} sec")
            return self

    def have_role(self, role_name):
        return role_name in self.roles

    def is_authenticated(self):
        if self.id_order < 1:
            return False
        else:
            return True

    def is_active(self):
        if self.id_order > 0:
            return True
        else:
            return False

    def is_anonymous(self):
        if self.id_order < 1:
            return True
        else:
            return False

    def get_id(self):
        return self.num_order

    def set_answered(self, num_answer):
        if num_answer not in self.list_answer:
            self.list_answer.append(num_answer)

    def get_answered(self):
        return self.list_answer


@login_manager.user_loader
def loader_user(num_order):
    if cfg.debug_level > 3:
        log.debug(f"LM. Loader User: {num_order}")
    return User().get_user_by_num_order(num_order, session['language'])


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    log.info(f"LM. LOGOUT. NUM_ORDER: {User().num_order}, IIN: {User().iin}, ip_addr: {User().ip_addr}")
    logout_user()
    return redirect(url_for('view_index'))


@app.after_request
def redirect_to_signing(response):
    if response.status_code == 401:
        return redirect(url_for('view_index') + '?next=' + request.url)
    return response
    

@app.before_request
def before_request():
    g.user = current_user


# @app.context_processor
# def get_current_user():
    # if g.user.id_user:
    # if g.user.is_anonymous:
    #     log.debug('Anonymous current_user!')
    # if g.user.is_authenticated:
    #     log.debug('Authenticated current_user: '+str(g.user.username))
    # return{"current_user": 'admin_user'}
