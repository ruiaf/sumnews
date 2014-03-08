import socket
import pickle
import logging

class BackendInterface:
    @staticmethod
    def retrieve(request):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            sock.connect(("localhost", 8001))
            sock.sendall(pickle.dumps(request))
            response = pickle.loads(sock.recv(1024))
            response["result"] = "success"
            logging.info("Request: " + str(request) + " Response: " + str(response))
            sock.close()
        except:
            return {"result": "error"}

        return response