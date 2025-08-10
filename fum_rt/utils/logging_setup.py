
import logging, json, os, sys, time

class JsonFormatter(logging.Formatter):
    def format(self, record):
        base = {
            "ts": time.time(),
            "level": record.levelname,
            "msg": record.getMessage(),
        }
        if record.__dict__.get("extra"):
            base.update(record.__dict__["extra"])
        return json.dumps(base, ensure_ascii=False)

def get_logger(name, log_file=None):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(JsonFormatter())
        logger.addHandler(sh)
        if log_file:
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            fh = logging.FileHandler(log_file)
            fh.setFormatter(JsonFormatter())
            logger.addHandler(fh)
    return logger
