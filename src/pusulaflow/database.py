import os
from pusulaflow.config import PROJECT_ROOT

import psycopg
from dotenv import load_dotenv
from pgvector.psycopg import register_vector

def get_connection(autocommit:bool=False,register_vector_types: bool=True):
    env_path = PROJECT_ROOT / ".env"
    load_dotenv(env_path)

    connection = psycopg.connect(
        host=os.environ["PGHOST"],
        port=int(os.environ["PGPORT"]),
        dbname=os.environ["PGDATABASE"],
        user=os.environ["PGUSER"],
        password=os.environ["PGPASSWORD"],
        connect_timeout=10,
        autocommit=autocommit,
    )

    try:
        if register_vector_types:
            register_vector(connection)
    except Exception:
        connection.close()
        raise

    return connection

def get_index(connection, index_name: str) -> dict:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                id,
                name,
                embedding_model,
                embedding_dimension,
                document_prefix,
                query_prefix,
                chunk_size,
                chunk_overlap
            FROM rag_indexes
            WHERE name = %s
            """,
            (index_name,),
        )

        row = cursor.fetchone()

        if row is None:
            raise ValueError(f"İndeks bulunamadı: {index_name}")

        columns = [column.name for column in cursor.description]

        return dict(zip(columns, row))

def get_chunk_hashes(connection, index_id: int) -> dict[str, str]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT id, content_hash
            FROM rag_chunks
            WHERE index_id = %s
            """,
            (index_id,),
        )

        return dict(cursor.fetchall())

def save_chunks(connection, index_id: int, chunks: list[dict]) -> None:
    if not chunks:
        return

    rows = [
        (
            index_id,
            chunk["id"],
            chunk["document_id"],
            chunk["chunk_position"],
            chunk["source"],
            chunk["text"],
            chunk["content_hash"],
            chunk["embedding"],
        )
        for chunk in chunks
    ]

    with connection.cursor() as cursor:
        cursor.executemany(
            """
            INSERT INTO rag_chunks (
                index_id,
                id,
                document_id,
                chunk_position,
                source,
                text,
                content_hash,
                embedding
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (index_id, id)
            DO UPDATE SET
                document_id = EXCLUDED.document_id,
                chunk_position = EXCLUDED.chunk_position,
                source = EXCLUDED.source,
                text = EXCLUDED.text,
                content_hash = EXCLUDED.content_hash,
                embedding = EXCLUDED.embedding
            """,
            rows,
        )

def search_chunks(
    connection,
    index_id: int,
    query_vector,
    top_k: int = 3,
) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                id,
                document_id,
                chunk_position,
                source,
                text,
                1 - (embedding <=> %s) AS vector_score
            FROM rag_chunks
            WHERE index_id = %s
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (query_vector, index_id, query_vector, top_k),
        )

        columns = [column.name for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def load_index_chunks(connection, index_id: int) -> list[dict]:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                id,
                document_id,
                chunk_position,
                source,
                text
            FROM rag_chunks
            WHERE index_id = %s
            ORDER BY document_id, chunk_position
            """,
            (index_id,),
        )

        columns = [column.name for column in cursor.description]

        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]

def delete_chunks(
    connection,
    index_id: int,
    chunk_ids: list[str],
) -> int:
    if not chunk_ids:
        return 0

    with connection.cursor() as cursor:
        cursor.execute(
            """
            DELETE FROM rag_chunks
            WHERE index_id = %s
              AND id = ANY(%s)
            """,
            (index_id, chunk_ids),
        )

        return cursor.rowcount

def validate_index_model(index: dict, expected_model: str) -> None:
    stored_model = index["embedding_model"]

    if stored_model != expected_model:
        raise ValueError(
            "Embedding modeli indeksle uyuşmuyor. "
            f"Yapılandırılan model: {expected_model}, "
            f"indeksin modeli: {stored_model}. "
            "Yeni model için ayrı bir indeks oluşturulmalı."
        )