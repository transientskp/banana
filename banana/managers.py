from django.db import models
from django.utils.datastructures import SortedDict


distance_query = """
ACOS(SIN(wm_decl)*SIN(%s) + COS(wm_decl)*COS(%s)*COS(wm_ra-%s))
"""


class RunningcatalogManager(models.Manager):
    def near_position(self, wm_ra, wm_decl, radius):
        """
        Return a QuerySet containing those objects within radius of ra, dec.
        All arguments should be given in radians.

        The returned fields will have an extra attribute, distance, giving the
        angular separation in radians from the ra, dec supplied.
        """
        return super(RunningcatalogManager, self).get_query_set().filter(
            wm_decl__gte=wm_decl-radius, wm_decl__lte=wm_decl+radius
        ).extra(
            select={'distance':  distance_query},
            select_params=[wm_decl, wm_decl, wm_ra],
            where=[distance_query + ' <= %s'],
            params=[wm_decl, wm_decl, wm_ra, radius]
        )
