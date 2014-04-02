from coreux import settings


def edition_list(request):
    return {'editions': settings.editions}


def selected_edition(request):
    edition = request.session.get("edition", settings.default_edition)
    return {'edition': edition}