from SumNewsService import SumNewsService
from DocumentRepository import DocumentRepository
from FeedManager import FeedManager

def main():
    repository = DocumentRepository()
    feed_manager = FeedManager()
    feed_manager.setup([], repository)
    feed_manager.start()
    news_service = SumNewsService(repository)
    news_service.Start()

if __name__ == "__main__":
    main()

