"""Modelin çağırabileceği araçlar ve ortak araç kaydı."""


def create_tools(documents, retriever):
    """Belgeleri ve arama indeksini araçlara bağlar."""

    def search_documents(query: str) -> list[dict]:
        """BM25 ve vektör aramasıyla ilgili belge parçalarını getirir.

        Sonuçlara aynı belgedeki komşu parçaları ek bağlam olarak ekler.
        Tam belgeyi okumak için sonuçtaki document_id kullanılabilir.

        Args:
            query: Bilgi ihtiyacını ifade eden arama sorgusu.
        """
        return retriever.search_documents(query)

    def list_documents() -> list[dict]:
        """Mevcut belgelerin kimliklerini ve kısa önizlemelerini listeler."""
        return [
            {'id': document['id'], 'preview': document['text'][:80]}
            for document in documents
        ]

    def read_document(document_id: str) -> dict:
        """Dosya adıyla belirtilen belgenin tam içeriğini getirir.

        Args:
            document_id: Belgenin dosya adı
        """
        for document in documents:
            if document['id'] == document_id:
                return document
        return {'error': 'Belge bulunamadı', 'document_id': document_id}
    return {
        'search_documents': search_documents,
        'list_documents': list_documents,
        'read_document': read_document,
    }
