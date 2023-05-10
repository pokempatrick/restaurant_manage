from django.test import SimpleTestCase
from django.urls import reverse, resolve

from dish_list import views


class TestUrls(SimpleTestCase):

    def test_dish_list_result_url_resolves(self):
        url = reverse('dish_list_result', args=["15"])
        self.assertEquals(resolve(url).func.view_class,
                          views.DishListResultAPIRUDView)

    def test_dish_list_result_validation_url_resolves(self):
        url = reverse('validations_dish_result', args=["15"])
        self.assertEquals(resolve(url).func.view_class,
                          views.ValidationAPIView)
