# -*- coding: utf-8 -*-

import django_filters
from django_filters.filters import Filter
from django.utils.safestring import mark_safe
from django.forms import BooleanField
from banana.models import AugmentedRunningcatalog


class NotNullFilter(Filter):
    """
    A boolean filter which filters on is null or not is null.
    """
    field_class = BooleanField

    def filter(self, qs, value):
        """
        if value is not None:
            return qs.filter(**{self.name + '__isnull': not value})
        """
        if value:
            return qs.filter(**{self.name + '__isnull': False})
        return qs


class RunningcatalogFilter(django_filters.FilterSet):
    """
    the django-filter logic used in the runningcatalog view.
    """
    sigma_min = django_filters.RangeFilter(name='sigma_min')
    sigma_max = django_filters.RangeFilter(name='sigma_max')
    wm_ra = django_filters.RangeFilter(label='Ra(°)')
    wm_decl = django_filters.RangeFilter(label='Dec(°)')
    v_int = django_filters.RangeFilter(name='v_int',
                                       label=mark_safe('V<sub>ν</sub>'))
    eta_int = django_filters.RangeFilter(name='eta_int',
                                         label=mark_safe('η<sub>ν</sub>'))
    newsource = NotNullFilter(name='newsource')

    class Meta:
        model = AugmentedRunningcatalog
        fields = ['wm_ra', 'wm_decl', 'newsource', 'v_int', 'eta_int']
