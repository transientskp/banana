import json
from django.test import TestCase
from django.core.urlresolvers import reverse
from banana.models import Extractedsource

test_db = 'default'


class ViewTest(TestCase):
    """
    test if all views are working
    """
    list_views = [
        'datasets',
        'images',
        'newsources',
        'extractedsources',
        'runningcatalogs',
        'varmetrics',
        'monitors',
        'skyregions',
        'configs',
    ]

    detail_views = [
        'newsource',
        'dataset',
        'extractedsource',
        'runningcatalog',
        'image',
        'bigimage',
        'monitor',
        'skyregion',
    ]

    def test_database_view(self):
        response = self.client.get(reverse('databases',))
        self.assertEqual(response.status_code, 200)

    def test_list_views(self):
        for list_view in self.list_views:
            try:
                response = self.client.get(reverse(list_view,
                                                   kwargs={'db': test_db}))
            except:
                print("problem with view %s" % list_view)
                raise
            self.assertEqual(response.status_code, 200)

    def test_list_csv_views(self):
        for list_view in self.list_views:
            try:
                response = self.client.get(reverse(list_view, kwargs={'db': test_db}) + "?format=csv")
            except:
                print("problem with csv view %s" % list_view)
                raise
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'text/csv')
            for row in response.content.split():
                columns = row.split(',')

    def test_list_json_views(self):
        for list_view in self.list_views:
            response = self.client.get(reverse(list_view,
                                               kwargs={'db': test_db}) +
                                       "?format=json")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['content-type'], 'application/json')
            try:
                json.loads(response.content)
            except ValueError as e:
                self.fail("can't parse json view %s: %s" % (list_view, e))

    def test_list_views_with_dataset(self):
        for list_view in self.list_views:
            try:
                response = self.client.get(reverse(list_view,
                                                   kwargs={'db': test_db}) +
                                           "?dataset=1")
            except Exception as e:
                print "problem with " + list_view
                raise

            self.assertEqual(response.status_code, 200)

    def test_detail_views(self):
        for detail_view in self.detail_views:
            try:
                response = self.client.get(reverse(detail_view,
                                                   kwargs={'db': test_db,
                                                           'pk': 1}))
            except Exception as e:
                print "%s detail view failed" % detail_view
                raise
            self.assertEqual(response.status_code, 200, "%s view didn't give 200" %
                             detail_view)

    def test_extracted_sources_pixel(self):
        response = self.client.get(reverse('extracted_sources_pixel',
                                           kwargs={'db': test_db,
                                                   'image_id': 1}))
        self.assertEqual(response.status_code, 200)

    def test_extractedsource_plot(self):
        response = self.client.get(reverse('extractedsource_plot',
                                           kwargs={'db': test_db,
                                                   'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_image_plot(self):
        response = self.client.get(reverse('image_plot',
                                           kwargs={'db': test_db,
                                                   'pk': 1}))
        self.assertEqual(response.status_code, 200)

    def test_csv_extractedsources_num(self):
        response = self.client.get(reverse('extractedsources',
                                           kwargs={'db': test_db}) +
                                   "?format=csv")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['content-type'], 'text/csv')

        returned_ids = []
        for line in response.content.split('\n'):
            line = line.strip()
            if line and not line.startswith('#'):
                returned_ids.append(line.split(',')[0])
        db_ids = Extractedsource.objects.using(test_db).all().values('id')
        self.assertEqual(len(returned_ids), len(db_ids))
