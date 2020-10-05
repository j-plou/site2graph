import logging

from twisted.python.failure import Failure

logger = logging.getLogger(__name__)


class MyDownloaderMiddleware:
    """
    This captures any exception as a Failure so it can be
    handled in errback.

    It's not obvious that this can be done, see _handle_downloader_output in
    https://github.com/scrapy/scrapy/blob/master/scrapy/core/engine.py
    """
    def process_request(self, request, spider):
        return None

    def process_response(self, request, response, spider):
        return response

    def process_exception(self, request, exception, spider):
        # logger.info("WAZZAP {0} {1}".format(type(exception), exception))

        return Failure(exception)
