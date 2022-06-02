# sqlalchemy-asyncpg-advisory-lock-int64

Tests that the `func.pg_advisory_xact_lock()` function in SQLAlchemy accepts an `int64` value as lock ID.

Currently failing for SQLAlchemy 1.4.

## Testing

```shell
docker compose up -d
poetry run python advisory_lock.py
```
