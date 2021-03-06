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
            data = []
            buffer = sock.recv(1024)
            while buffer:
                data.append(buffer)
                buffer = sock.recv(1024)
            response = pickle.loads(bytes().join(data))
            logging.info("Request: " + str(request) + " Response: " + str(response))
            sock.close()
        except ValueError as inst:
            logging.error(inst)
            return {"result": "error"}

        return response