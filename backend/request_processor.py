"""
Process requests received
"""

import logging
import time


class RequestProcessor(object):
    """
    Process requests received
    """

    @staticmethod
    def process(document_repository, request):
        """
        Process requests received
        """
        logging.info("Processing request: %s", request['type'])
        ts = time.time()

        response = {'result': 'error'}

        if request['type'] == "latest_news":
            response = {
                "result": "success",
                "content": [doc.as_dictionary() for doc in document_repository.recent_documents()]
            }

        if request['type'] == "latest_clusters":
            results = []
            for cluster in document_repository.recent_clusters():
                result = []
                for doc in cluster:
                    result.append(doc.as_dictionary())
                results.append(result)

            response = {
                "result": "success",
                "content": results
            }

        if request['type'] == "search_clusters":
            results = []
            for cluster in document_repository.search_clusters(request['query']):
                result = []
                for doc in cluster:
                    result.append(doc.as_dictionary())
                results.append(result)

            response = {
                "result": "success",
                "content": results
            }

        if request['type'] == "search":
            response = {
                "result": "success",
                "content": [doc.as_dictionary() for doc in document_repository.search(request['query'])]
            }

        if request['type'] == "search_guid":
            doc = document_repository.search_guid(request['guid'])
            if not doc:
                return response
            response = {
                "result": "success",
                "content": {
                    'article': doc.as_dictionary(),
                    'children': [c.as_dictionary() for c in doc.children],
                }
            }

            if doc.exemplar != doc:
                response['content']['parent'] = doc.exemplar.as_dictionary()
                response['content']['siblings'] = [s.as_dictionary() for s in doc.exemplar.children]


        te = time.time()
        logging.info("Finished processing after %2.2f ms.", (te-ts)*1000)
        return response
