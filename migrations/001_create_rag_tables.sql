CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE rag_indexes (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    embedding_model TEXT NOT NULL,
    embedding_dimension INTEGER NOT NULL
        CHECK (embedding_dimension > 0),
    document_prefix TEXT NOT NULL,
    query_prefix TEXT NOT NULL,
    chunk_size INTEGER NOT NULL
        CHECK (chunk_size > 0),
    chunk_overlap INTEGER NOT NULL
        CHECK (chunk_overlap >= 0 AND chunk_overlap < chunk_size),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE rag_chunks (
    index_id BIGINT NOT NULL REFERENCES rag_indexes(id),
    id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    chunk_position INTEGER NOT NULL CHECK (chunk_position >= 0),
    source TEXT NOT NULL,
    text TEXT NOT NULL,
    content_hash TEXT NOT NULL,
    embedding VECTOR(768) NOT NULL,

    PRIMARY KEY (index_id, id),
    UNIQUE (index_id, document_id, chunk_position)
);

