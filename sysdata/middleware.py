import logging

logger=logging.getLogger('sysdata.middleware')

class ExceptionMiddleware(object):
    def process_exception(self, request, exception):
        logger.error("report error:",exc_info=1)