"""
Custom SQL aggregate functions
"""
from django.db.models import Aggregate
from django.db.models.sql.aggregates import Aggregate as AggregateSql, Avg
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class MedianSql(AggregateSql):
    sql_function = 'MEDIAN'


class Median(Aggregate):
    """
    This return the Median for a column. Note that not all databases (for
    example PostgreSQL) support this SQL function. This means you need to add
    this function manually.
    """
    name = 'Median'

    def add_to_query(self, query, alias, col, source, is_summary):
        klass = MedianSql
        # TODO: this is a hack for now, SQLite doesn't support median and
        # custom functions so we just return the average in case of testing
        logger.warning('Detected test run, using avg() SQL function, not median()')
        if settings.TESTING:
            aggregate = Avg(col, source=source, is_summary=is_summary,
                            **self.extra)
        else:
            aggregate = klass(col, source=source, is_summary=is_summary,
                              **self.extra)
        query.aggregates[alias] = aggregate
