"""
Process requests received
"""

import logging


class RequestProcessor(object):
    """
    Process requests received
    """

    @staticmethod
    def process(document_repository, request):
        """
        Process requests received
        """
        logging.info("Processing request")

        response = {'result': 'error'}

        if request['type'] == "latest_news":
            response = {
                "result": "success",
                "content": document_repository.recent_documents()
            }

        if request['type'] == "search":
            response = {
                "result": "success",
                "content": document_repository.search(request['query'])
            }

        logging.info("Finished processing.")
        return response
