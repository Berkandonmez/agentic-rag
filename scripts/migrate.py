"""Veritabanı migration işlemlerini yönetir."""
from pusulaflow.database import get_connection
import hashlib
from pusulaflow.config import PROJECT_ROOT

import argparse


def ensure_migration_table(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rag_schema_migrations (
                filename TEXT PRIMARY KEY,
                checksum TEXT NOT NULL,
                applied_at TIMESTAMPTZ NOT NULL
                    DEFAULT CURRENT_TIMESTAMP
            )
        """)

def load_migrations() -> list[dict]:
    migrations_dir = PROJECT_ROOT / "migrations"
    paths = sorted(migrations_dir.glob("*.sql"))

    if not paths:
        raise ValueError("migrations klasöründe SQL dosyası bulunamadı.")

    migrations = []

    for path in paths:
        sql = path.read_text(encoding="utf-8-sig")

        if not sql.strip():
            raise ValueError(f"Migration dosyası boş: {path.name}")

        migrations.append({
            "filename": path.name,
            "sql": sql,
            "checksum": hashlib.sha256(
                sql.encode("utf-8")
            ).hexdigest(),
        })

    return migrations

def get_applied_migrations(connection) -> dict[str, str]:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT filename, checksum
            FROM rag_schema_migrations
        """)

        return dict(cursor.fetchall())

def record_migration(connection, migration: dict) -> None:
    with connection.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO rag_schema_migrations (filename, checksum)
            VALUES (%s, %s)
            """,
            (migration["filename"], migration["checksum"]),
        )

def apply_migration(connection, migration: dict) -> None:
    with connection.cursor() as cursor:
        cursor.execute(migration["sql"])

    record_migration(connection, migration)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--baseline",
        action="store_true",
        help="Önceden doğrulanmış mevcut kurulumu geçmişe kaydeder.",
    )
    args = parser.parse_args()

    migrations = load_migrations()

    with get_connection(register_vector_types=False) as connection:
        ensure_migration_table(connection)
        applied = get_applied_migrations(connection)

        pending = []

        for migration in migrations:
            filename = migration["filename"]

            if filename not in applied:
                pending.append(migration)
            elif applied[filename] != migration["checksum"]:
                raise ValueError(
                    f"Uygulanmış migration değiştirilmiş: {filename}"
                )

        if args.baseline:
            expected_files = {
                "001_create_rag_tables.sql",
                "002_seed_rag_index.sql",
            }

            found_files = {
                migration["filename"]
                for migration in migrations
            }

            if applied or found_files != expected_files:
                raise ValueError(
                    "Bu başlangıç işlemi yalnızca geçmiş boşken "
                    "ve doğruladığımız iki migration için kullanılabilir."
                )

            for migration in pending:
                record_migration(connection, migration)

            print("Mevcut kurulum baseline olarak kaydedildi.")
            return

        print("Bulunan migration sayısı:", len(migrations))
        print("Geçmişte kayıtlı migration sayısı:", len(applied))
        print("Bekleyen migration sayısı:", len(pending))
        for migration in pending:
            print("Uygulanıyor:", migration["filename"])
            apply_migration(connection, migration)

    print("Migration işlemi tamamlandı.")
if __name__ == "__main__":
    main()