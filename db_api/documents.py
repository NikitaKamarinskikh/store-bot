from web.documents.models import Documents


def get_document_by_type(type: str) -> Documents:
    return Documents.objects.get(type=type)

