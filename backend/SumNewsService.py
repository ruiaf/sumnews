import socketserver
import pickle
from RequestProcessor import RequestProcessor
import settings
import logging

class SumNewsService:
        def __init__(self, document_repository, host=settings.NEWS_SERVICE_HOST, port=settings.NEWS_SERVICE_PORT):
            self.document_repository = document_repository
            self.host = host
            self.port = port

        def Start(self):
            server = socketserver.TCPServer((self.host, self.port), SumNewsRequestHandler)
            server.document_repository = self.document_repository
            logging.info("Serving SumNewsService at Port: %s" % self.port)
            server.serve_forever()

class SumNewsRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request_msg = pickle.loads(self.request.recv(settings.PACKET_MAX_SIZE))
        response_msg = RequestProcessor.Process(self.server.document_repository, request_msg)
        self.request.sendall(pickle.dumps(response_msg))