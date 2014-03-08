import socketserver
import pickle
from datetime import datetime, timedelta

def main():
    run_server()

def run_server(host="", port=8001):
    server = socketserver.TCPServer((host, port), SumNewsRequestHandler)

    print("Serving at Port", port)
    server.serve_forever()

class SumNewsRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        request_msg = pickle.loads(self.request.recv(1024))
        print(request_msg)

        response_msg = { "result" : "success",
                         "content" :
                             [{'title': 'one piece of news title',
                               'date': datetime.now() - timedelta(minutes = 10),
                               'content': 'a piece of news retrieved from the backend'},
                              {'title': 'second piece of news title',
                               'date': datetime.now() - timedelta(hours = 50),
                               'content': 'another piece of news retrieved from the backend'}]
        }

        self.request.sendall(pickle.dumps(response_msg))

if __name__ == "__main__":
    main()
