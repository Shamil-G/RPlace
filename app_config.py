from pdd_parameter import using, app_name

if using == 'DEV_WIN_HOME':
    BASE = f'D:/Shamil/{app_name}'
elif using == 'DEV_WIN':
    BASE = f'C:/Shamil/{app_name}'
else:
    BASE = f'/home/pdd/{app_name}'

if using[0:7] != 'DEV_WIN':
    host = 'pdd_1'
    os = 'unix'
    debug_level = 2
    FACE_CONTROL_ENABLE = True
    port = 5015
else:
    os = '!unix'
    debug_level = 4
    FACE_CONTROL_ENABLE = True
    host = 'localhost'
    port = 83

PHOTO = f'{BASE}/static/photo'
LIVE_PHOTO = f'{BASE}/live-photo'
PICTURES = '/static/pictures'
LOG_FILE = f'{BASE}/random-place.log'
IMAGE_TYPE = '!base64'
#RECOGNITION_HOST = '127.0.0.1'
RECOGNITION_HOST = '10.51.203.169'
PORT_FACE_CONTROL = '4001'
RECOGNITION_CONTEXT = 'api/predict2'
HOST_BUS = '10.51.203.140'
PORT_TO_ARM_GO = '4200'
DIVIDER_FACE_CONTROL = 3
QUALITY = 88
debug = True
language = 'ru'
src_lang = 'file'
trace_malloc = False
move_at_once = False

print(f"=====> CONFIG. using: {using}, BASE: {BASE}, app_name: {app_name}")
