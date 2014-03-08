import logging
import settings

class RequestProcessor:
    @staticmethod
    def Process(document_repository, request_msg):
        logging.info("Processing request")

        response_msg = {'result' : 'error'}

        if request_msg['type'] == "latest_news":
                response_msg = { "result" : "success",
                                 "content" : document_repository.recentDocuments()
                }

        logging.info("Finished processing.")
        return response_msg
