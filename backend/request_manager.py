"""
Starts a TCP server and listens for requests
"""

import socketserver
import pickle
import logging

from request_processor import RequestProcessor
import settings


class RequestListner(object):
    """
    CP server to listen for requests
    """

    def __init__(self, document_repository,
                 host=settings.NEWS_SERVICE_HOST,
                 port=settings.NEWS_SERVICE_PORT):
        self.document_repository = document_repository
        self.host = host
        self.port = port

    def start(self):
        """
        Start server to listen for requests and hang, listening for requests
        """
        server = socketserver.TCPServer((self.host, self.port), RequestHandler)
        server.document_repository = self.document_repository
        logging.info("Serving SumNewsService at Port: %s", self.port)
        server.serve_forever()


class RequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        """
        Handle a request
        """

        # deserialize the request
        request_msg = pickle.loads(self.request.recv(settings.PACKET_MAX_SIZE))

        # process the request
        response_msg = RequestProcessor.process(
            self.server.document_repository,
            request_msg)

        # serialize and send the response
        self.request.sendall(pickle.dumps(response_msg))
