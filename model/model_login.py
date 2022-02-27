from flask import redirect, g, Response, session, url_for, request, json
from flask_login import login_user
from main_app import log
from main_config import cfg
import requests
import cx_Oracle
from db_oracle.connect import get_connection, plsql_proc, plsql_proc_s
from db_oracle.UserLogin import User
import os


if __name__ == "__main__":
    log.debug("Тестируем get order")
    # get_order(-100)

