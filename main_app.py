from __init__ import app, log
import app_config as cfg
# Don't remove below lines. There are APP routes
from view import routes


if __name__ == "__main__":
    # cors = CORS(app, resources={r"/checkImage2/*": {"origins": "*"}})
    app.run(host=cfg.host, port=cfg.port, debug=False)
    log.info("===> Main Application started")
