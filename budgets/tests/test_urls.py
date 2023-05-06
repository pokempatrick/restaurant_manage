from django.test import SimpleTestCase
from django.urls import reverse, resolve

from budgets import views


class TestUrls(SimpleTestCase):

    def test_validations_url_resolves(self):
        url = reverse('validations_budget', args=["15"])
        self.assertEquals(resolve(url).func.view_class,
                          views.ValidationAPIView)
