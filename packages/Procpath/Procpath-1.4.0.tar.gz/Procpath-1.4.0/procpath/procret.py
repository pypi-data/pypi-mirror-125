import json
from contextlib import closing
from datetime import datetime
from typing import List, Mapping, NamedTuple


try:
    import apsw as sqlite
    from apsw import SQLError as SqlError
except ImportError:  # nocov
    import sqlite3 as sqlite
    from sqlite3 import OperationalError as SqlError


__all__ = 'create_query', 'query', 'registry', 'Query', 'QueryError', 'QueryExecutionError'

registry = {}


class QueryError(Exception):
    """General query error."""


class QueryExecutionError(Exception):
    """SQL query execution error."""


class Query(NamedTuple):
    query: str
    title: str

    min_version: tuple = (1,)
    """Minimal SQLite version compatible with the query."""

    procfile_required: frozenset = frozenset()
    """Procfiles required by the query. ``stat`` is assumed."""


def create_query(value_expr: str, title: str, **kwargs) -> Query:
    return Query(
        f'''
        SELECT
            ts,
            stat_pid pid,
            {value_expr} value
        FROM record
        WHERE
            (:after IS NULL OR :after <= ts)
            AND (:before IS NULL OR ts <= :before)
            AND (:pid_list IS NULL OR instr(:pid_list, ',' || stat_pid || ','))
        ORDER BY stat_pid, record_id
        ''',
        title,
        **kwargs,
    )


def query(
    database: str,
    query: Query,
    after: datetime = None,
    before: datetime = None,
    pid_list: List[int] = None,
) -> List[Mapping]:
    conn = sqlite.Connection(database)
    cursor = conn.cursor()

    sqlite_version = cursor.execute('SELECT sqlite_version()').fetchone()[0]
    sqlite_version = tuple(map(int, sqlite_version.split('.')))
    if sqlite_version < query.min_version:
        raise QueryError(
            f'{query.title!r} requires SQLite version >= {query.min_version}, '
            f'installed {sqlite_version}. Install apsw-wheels and try again.'
        )

    if query.procfile_required:
        sql = "SELECT value FROM meta WHERE key = 'procfile_list'"
        procfile_list = cursor.execute(sql).fetchone()
        procfile_provided = set(json.loads(procfile_list[0])) if procfile_list else set()
        missing = ', '.join(sorted(query.procfile_required - procfile_provided))
        if missing:
            raise QueryError(
                f'{query.title!r} requires the following procfiles missing '
                f'in the database: {missing}'
            )

    row_factory = lambda cur, row: dict(zip([t[0] for t in cur.description], row))
    try:
        conn.row_factory = row_factory
    except AttributeError:
        conn.setrowtrace(row_factory)

    with closing(conn):
        cursor = conn.cursor()
        try:
            cursor.execute(query.query, {
                'after': after.timestamp() if after else None,
                'before': before.timestamp() if before else None,
                'pid_list': ',{},'.format(','.join(map(str, pid_list))) if pid_list else None,
            })
        except SqlError as ex:
            raise QueryExecutionError(str(ex)) from ex
        else:
            return cursor.fetchall()


registry['cpu'] = Query(
    '''
    WITH diff AS (
        SELECT
            record_id,
            ts,
            stat_pid,
            stat_utime + stat_stime - LAG(stat_utime + stat_stime) OVER (
                PARTITION BY stat_pid
                ORDER BY record_id
            ) tick_diff,
            ts - LAG(ts) OVER (
                PARTITION BY stat_pid
                ORDER BY record_id
            ) ts_diff
        FROM record
    )
    SELECT
        ts,
        stat_pid pid,
        100.0 * tick_diff / (SELECT value FROM meta WHERE key = 'clock_ticks') / ts_diff value
    FROM diff
    WHERE
        tick_diff IS NOT NULL
        AND (:after IS NULL OR :after <= ts)
        AND (:before IS NULL OR ts <= :before)
        AND (:pid_list IS NULL OR instr(:pid_list, ',' || stat_pid || ','))
    ORDER BY stat_pid, record_id
    ''',
    'CPU usage, %',
    min_version=(3, 25),
)

registry['rss'] = create_query(
    "stat_rss / 1024.0 / 1024 * (SELECT value FROM meta WHERE key = 'page_size')",
    'Resident Set Size, MiB',
)

registry['pss'] = create_query(
    "smaps_rollup_pss / 1024.0",
    'Proportional Set Size, MiB',
    procfile_required=frozenset(['smaps_rollup']),
)

registry['uss'] = create_query(
    "(smaps_rollup_private_clean + smaps_rollup_private_dirty) / 1024.0",
    'Unique Set Size, MiB',
    procfile_required=frozenset(['smaps_rollup']),
)
