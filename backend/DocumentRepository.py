class DocumentRepository:
    def __init__(self):
        self.documents = []

    def add(self, document_list):
        self.documents.extend(document_list)

    def recentDocuments(self, count=10):
        count = min(count, len(self.documents))
        return  self.documents[:count]