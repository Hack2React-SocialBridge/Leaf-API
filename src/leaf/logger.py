import logging

from leaf.dependencies import get_settings


settings = get_settings()


class RequestLogFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        for arg in ("url", "method", "ip", "user"):
            if not hasattr(record, arg):
                setattr(record, arg, "")
        return super().format(record)


logger = logging.getLogger()
logger.setLevel(settings.LOG_LEVEL)
formatter = RequestLogFormatter(
    fmt="%(levelname)s\t %(asctime)s - %(msg)s [url=%(url)s, method=%(method)s, ip=%(ip)s, user=%(user)s]"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)