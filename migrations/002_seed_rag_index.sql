INSERT INTO rag_indexes (
    name,
    embedding_model,
    embedding_dimension,
    document_prefix,
    query_prefix,
    chunk_size,
    chunk_overlap
)
VALUES (
    'company_docs_v1',
    'embeddinggemma:300m',
    768,
    'title: {document_id} | text: {text}',
    'task: search result | query: {query}',
    100,
    20
)
ON CONFLICT (name) DO NOTHING;