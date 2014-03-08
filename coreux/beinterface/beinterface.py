import socket
import sys
import pickle
import logging

class BackendInterface:
    @staticmethod
    def retrieve(request):
        # Create a socket (SOCK_STREAM means a TCP socket)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(("localhost", 8001))
            sock.sendall(pickle.dumps(request))
            response = pickle.loads(sock.recv(1024))
            response["result"] = "success"
            logging.info("Request: " + str(request) + " Response: " + str(response))
            return response
        finally:
            sock.close()

        return {"result": "error"}