from coreux import settings

class EditionMiddleware:
    @staticmethod
    def process_request(request):
        if not "edition" in request.session:
            request.session["edition"] = settings.default_edition