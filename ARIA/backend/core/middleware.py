import logging, time
from flask import request, g, jsonify
from backend.core.exceptions import AppError

log = logging.getLogger("aria.http")

def init_middleware(app):
    @app.before_request
    def _start(): g.t0 = time.time()
    @app.after_request
    def _log(resp):
        log.info("%s %s %s %.0fms", request.method, request.path, resp.status_code, (time.time() - g.get("t0", time.time())) * 1000)
        return resp
    @app.errorhandler(AppError)
    def _err(e): return jsonify(error=e.message), e.status
