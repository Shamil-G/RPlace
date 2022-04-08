from main_app import app, log
import app_config as cfg
from view.i18n import i18n
from db_oracle.connect import get_connection
from flask import send_from_directory, session, redirect, url_for, request
import tracemalloc
import os
# from test_memory import start_thread
import psutil


s = None


@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    if cfg.debug_level > 0:
        log.debug(f"file for upload: {cfg.REPORTS_PATH}/{filename}")
    return send_from_directory(cfg.REPORTS_PATH, filename)


@app.route('/language/<string:lang>')
def set_language(lang):
    session['language'] = lang
    # Получим предыдущую страницу, чтобы на неё вернуться
    current_page = request.referrer
    if current_page is not None:
        return redirect(current_page)
    else:
        return redirect(url_for('view_index'))


@app.context_processor
def utility_processor():
    if cfg.debug_level > 3:
        log.debug(f"Context processor: {get_i18n_value('APP_NAME')}")
    return dict(res_value=get_i18n_value)


def get_i18n_value(res_name):
    if 'language' in session:
        lang = session['language']
    else:
        lang = cfg.language
        session['language'] = cfg.language
    if cfg.src_lang == 'db':
        con = get_connection()
        cursor = con.cursor()
        return_value = cursor.callfunc("GET I18n Value", str, [lang, res_name])
        cursor.close()
        con.close()
    if cfg.src_lang == 'file':
        return_value = i18n.get_resource(lang, res_name)
    if cfg.debug_level > 4:
        log.debug(f'Get i18N Value. lang: {lang}, res_name: {res_name} value: {return_value}')
    return return_value


@app.route('/memory')
def print_memory():
    return {'memory': psutil.Process(os.getpid()).memory_info().rss}


@app.route("/snapshot")
def snap():
    global s
    if cfg.trace_malloc:
        if not s:
            s = tracemalloc.take_snapshot()
            return "taken snapshot\n"
        else:
            lines = []
            top_stats = tracemalloc.take_snapshot().compare_to(s, 'lineno')
            for stat in top_stats[:25]:
                lines.append(str(stat))
            return "\n".join(lines)


def print_memory(fn):
    def wrapper(*args, **kwargs):
        pr = psutil.Process(os.getpid())
        pr.memory_info()
        try:
            start_mem = pr.memory_info()
            # log.debug(f'===============> Start {fn.__name__.upper()}: {start_mem}')
            return fn(*args, **kwargs)
        finally:
            finish_mem = pr.memory_info()
            # log.debug(f'-----memory----> Stop  {fn.__name__.upper()}: {finish_mem}')
            log.debug(f'-----memory----> DEBUG {fn.__name__.upper()}: '
                      f'rss({finish_mem.rss-start_mem.rss}), '
                      f'vms({finish_mem.vms-start_mem.vms})'
                      #f'num_page_faults({finish_mem.num_page_faults-start_mem.num_page_faults}), '
                      #f'peak_wset({finish_mem.peak_wset-start_mem.peak_wset}), '
                      #f'wset({finish_mem.wset-start_mem.wset}), '
                      #f'peak_paged_pool({finish_mem.peak_paged_pool-start_mem.peak_paged_pool}), '
                      #f'paged_pool({finish_mem.paged_pool-start_mem.paged_pool}), '
                      #f'peak_nonpaged_pool({finish_mem.peak_nonpaged_pool-start_mem.peak_nonpaged_pool}), '
                      #f'nonpaged_pool({finish_mem.nonpaged_pool-start_mem.nonpaged_pool}), '
                      #f'pagefile({finish_mem.pagefile-start_mem.pagefile}), '
                      #f'peak_pagefile({finish_mem.peak_pagefile-start_mem.peak_pagefile}), '
                      #f'private({finish_mem.private-start_mem.private}) '
                      )
    return wrapper



