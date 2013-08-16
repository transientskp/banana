from django.test import TestCase
from django.core.urlresolvers import reverse

test_db = 'default'


class ViewTest(TestCase):
    """
    test if all views are working
    """
    list_views = [
        'datasets',
        'images',
        'transients',
        'extractedsources',
        'runningcatalogs',
        'monitoringlists',
    ]

    def test_database_view(self):
        response = self.client.get(reverse('databases',))
        self.assertEqual(response.status_code, 200)

    def test_list_views(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}))
            self.assertEqual(response.status_code, 200)
