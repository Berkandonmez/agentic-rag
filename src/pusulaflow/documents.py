"""Markdown belgelerini yükleme ve örtüşen parçalara ayırma."""
from pathlib import Path


def load_documents(data_dir: Path) -> list[dict]:
    """Klasördeki metin dosyalarını belge listesine dönüştürür."""
    documents = []
    for file_path in sorted(data_dir.glob('*.md')):
        text = file_path.read_text(encoding='utf-8')
        documents.append({'id': file_path.name, 'source': str(file_path), 'text': text})
    return documents


def chunk_documents(documents: list[dict], chunk_size: int=100, overlap: int=20) -> list[dict]:
    """Belgeleri örtüşen sözcük gruplarına ayırır."""
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError('chunk_size pozitif, overlap ise 0 ile chunk_size arasında olmalı.')
    chunks = []
    step = chunk_size - overlap
    for document in documents:
        words = document['text'].split()
        for start in range(0, len(words), step):
            chunk_text = ' '.join(words[start:start + chunk_size])
            chunks.append({'id': f"{document['id']}#chunk-{start // step + 1}", 'document_id': document['id'], 'source': document['source'], 'text': chunk_text})
            if start + chunk_size >= len(words):
                break
    return chunks
