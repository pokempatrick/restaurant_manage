from django.test import SimpleTestCase
from django.urls import reverse, resolve

from procurement import views


class TestUrls(SimpleTestCase):

    def test_procurement_url_resolves(self):
        url = reverse('procurements', args=["15"])
        self.assertEquals(resolve(url).func.view_class,
                          views.ProcurementsAPIRUDView)

    def test_procurement_validaiton_url_resolves(self):
        url = reverse('validations_procurements', args=["15"])
        self.assertEquals(resolve(url).func.view_class,
                          views.ValidationAPIView)
