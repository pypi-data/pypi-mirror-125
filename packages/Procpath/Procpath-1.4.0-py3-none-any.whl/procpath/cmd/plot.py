import itertools
from datetime import datetime
from typing import List, Mapping, Tuple

from .. import plotting, procret
from . import CommandError


__all__ = 'run',


def _get_file_queries(filenames: list):
    for filename in filenames:
        with open(filename, 'r') as f:
            yield procret.Query(f.read(), 'Custom query')


def _get_expr_queries(exprs: list):
    for expr in exprs:
        yield procret.create_query(expr, 'Custom expression')


def _get_named_queries(names: list):
    for query_name in names:
        try:
            query = procret.registry[query_name]
        except KeyError:
            raise CommandError(f'Unknown query {query_name}')
        else:
            yield query


def _get_queries(
    query_name_list: list,
    custom_query_file_list: list,
    custom_value_expr_list: list,
    share_y_axis: bool,
):
    queries = []
    if query_name_list:
        queries.extend(_get_named_queries(query_name_list))
    if custom_value_expr_list:
        queries.extend(_get_expr_queries(custom_value_expr_list))
    if custom_query_file_list:
        queries.extend(_get_file_queries(custom_query_file_list))

    if not queries:
        raise CommandError('No query to plot')
    elif not share_y_axis and len(queries) > 2:
        raise CommandError('More than 2 queries to plot on 2 Y axes')

    return queries


def _get_pid_series_points(
    timeseries: List[Mapping],
    epsilon: float = None,
    moving_average_window: int = None,
) -> Mapping[int, List[Tuple[int, int]]]:
    pid_series = {}
    for pid, series in itertools.groupby(timeseries, lambda r: r['pid']):
        pid_series[pid] = [(r['ts'], r['value']) for r in series]
        if epsilon:
            pid_series[pid] = plotting.decimate(pid_series[pid], epsilon)
        if moving_average_window:
            x, y = zip(*pid_series[pid])
            pid_series[pid] = list(zip(
                plotting.moving_average(x, moving_average_window),
                plotting.moving_average(y, moving_average_window),
            ))

    return pid_series


def run(
    database_file: str,
    plot_file: str,
    query_name_list: list = None,
    after: datetime = None,
    before: datetime = None,
    pid_list: list = None,
    epsilon: float = None,
    moving_average_window: int = None,
    share_y_axis: bool = False,
    logarithmic: bool = False,
    style: str = None,
    formatter: str = None,
    title: str = None,
    custom_query_file_list: list = None,
    custom_value_expr_list: list = None,
):
    queries = _get_queries(
        query_name_list,
        custom_query_file_list,
        custom_value_expr_list,
        share_y_axis,
    )
    assert queries and (share_y_axis or len(queries) <= 2)

    pid_series_list = []
    for query in queries:
        try:
            timeseries = procret.query(database_file, query, after, before, pid_list)
        except procret.QueryExecutionError as ex:
            raise CommandError(f'SQL error: {ex}') from ex
        except procret.QueryError as ex:
            raise CommandError(str(ex)) from ex
        else:
            pid_series_list.append(
                _get_pid_series_points(timeseries, epsilon, moving_average_window)
            )

    if not title:
        if share_y_axis:
            title = '\n'.join(f'{i}. {q.title}' for i, q in enumerate(queries, start=1))
        elif len(queries) == 1:
            title = queries[0].title
        else:
            title = f'{queries[0].title} vs {queries[1].title}'

    plotting.plot(
        plot_file=plot_file,
        title=title,
        pid_series_list=pid_series_list,
        share_y_axis=share_y_axis,
        logarithmic=logarithmic,
        style=style,
        formatter=formatter,
    )
