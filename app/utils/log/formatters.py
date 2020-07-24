from datetime import datetime

from json_log_formatter import JSONFormatter


class APIJSONFormatter(JSONFormatter):
    def json_record(self, message, extra, record):
        extra['timestamp'] = datetime.now()
        extra['severity'] = record.levelname
        extra['module'] = record.name
        extra['method'] = record.funcName
        extra['message'] = message
        if record.exc_info:
            extra['exc_info'] = record.exc_info  # pragma: no cover
        return extra
