from django.db import models

distance_query = """
DEGREES(
    ACOS(
        SIN(RADIANS(wm_decl)) * SIN(RADIANS(%s)) +
        COS(RADIANS(wm_decl)) * COS(RADIANS(%s)) *
        COS(RADIANS(wm_ra) - RADIANS(%s))
    )
)
"""


class RunningcatalogManager(models.Manager):
    def near_position(self, ra, decl, radius):
        """
        Return a QuerySet containing those objects within radius of ra, dec.
        All arguments should be given in radians.

        The returned fields will have an extra attribute, distance, giving the
        angular separation in radians from the ra, dec supplied.
        """
        return super(RunningcatalogManager, self).get_query_set().filter(
            wm_decl__gte=decl-radius, wm_decl__lte=decl+radius,
            wm_ra__gte=ra-radius, wm_ra__lte=ra+radius
        ).extra(
            select={'distance':  distance_query},
            select_params=[decl, decl, ra],
            where=[distance_query + ' <= %s'],
            params=[decl, decl, ra, radius]
        )
