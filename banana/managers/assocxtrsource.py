from django.db import models, connections


def transient_query():
    """
    Return a SQL query for obtaining transients of a specific dataset with a
    minimum V and eta. You should execute this query with (in order)
    v_int and eta_int as argument.

    First we select the last time timstamps of the images per band and
    runningcatalog, this is the inner query. We then join this query with
    the runningcatalog again to obtain the corresponding assocxtrsource ID's.
    We can't do this all in one.
    """
    return """
SELECT
    assocxtrsource.id
FROM
    (runningcatalog
    JOIN assocxtrsource ON assocxtrsource.runcat = runningcatalog.id
    JOIN extractedsource ON assocxtrsource.xtrsrc = extractedsource.id
    JOIN image  ON extractedsource.image = image.id)
    JOIN (
        SELECT
            a.runcat as runcat_id,
            i.band as band,
            max(i.taustart_ts) as MaxTimestamp

        FROM
            assocxtrsource a
            JOIN extractedsource e ON a.xtrsrc = e.id
            JOIN image i ON e.image = i.id
        GROUP BY
            runcat_id, band
        ) last_timestamps
    ON  runningcatalog.id = last_timestamps.runcat_id
    AND image.band = last_timestamps.band
    AND image.taustart_ts = last_timestamps.MaxTimestamp
"""


class AssocxtrsourceManager(models.Manager):
    """
    The custom manager for banana.models.Assocxtrsource
    """
    def transients(self, v_int, eta_int, dataset):
        """
        Retrieves a list of transients with a minimal v and eta value for
        a specific dataset.

        Since it seems impossible to build this query using the Django ORM
        first we execute a Raw query that returns the assocxtrsource ID's.
        Then we use the ID's to convert it to a Django ResultSet. Not the
        optimal solution but it works.

        For optimisation the dataset ID is used here, since otherwise the
        results are returned for the full database.
        """
        query = transient_query()
        cursor = connections[self.db].cursor()

        raw_args = []
        if dataset:
            query += " AND image.dataset = %s"
            raw_args.append(dataset)

        if v_int:
            query += " AND assocxtrsource.v_int >= %s"
            raw_args.append(v_int)

        if eta_int:
            query += " AND assocxtrsource.eta_int >= %s"
            raw_args.append(eta_int)

        cursor.execute(query, raw_args)
        ids = [i[0] for i in cursor.fetchall()]
        related = ['runcat', 'xtrsrc', 'xtrsrc__image', 'xtrsrc__image__band']
        orm_args = {'id__in': ids}
        if v_int:
            orm_args['v_int__gt'] = v_int
        if eta_int:
            orm_args['eta_int__gt'] = eta_int
        return self.select_related(*related).filter(**orm_args)