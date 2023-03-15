# import json
#
# from django.test import TestCase
# from django.urls import reverse
#
#
# class DumpDataFixtureViewTests(TestCase):
#     def test_dumpdata_fixture(self):
#         url = reverse("dumpdata-fixture")
#         response = self.client.get(url)
#
#         self.assertEqual(response.status_code, 200)
#
#         data = json.loads(response.content)
#         self.assertIsNotNone(data)
