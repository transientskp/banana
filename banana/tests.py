from django.test import TestCase
from django.core.urlresolvers import reverse

test_db = 'default'


class ViewTest(TestCase):
    """
    test if all views are working
    """
    def test_database_list(self):
        response = self.client.get(reverse('databases',))
        self.assertEqual(response.status_code, 200)

    def test_dataset_list(self):
        response = self.client.get(reverse('datasets', kwargs={'db': test_db}))
        self.assertEqual(response.status_code, 200)

    def test_extractedsource_list(self):
        response = self.client.get(reverse('extractedsources',
                                           kwargs={'db': test_db}))
        self.assertEqual(response.status_code, 200)

