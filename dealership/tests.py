from urllib.parse import parse_qs, urlparse

from django.test import TestCase
from django.urls import reverse

from .models import Car, CustomCarRequest, Review


class CustomerFlowTests(TestCase):
    def make_car(self, status='available', name='QA Car'):
        return Car.objects.create(brand='QA', model_name=name, year=2020,
                                  mileage=100, price=10000, fuel='petrol',
                                  transmission='manual', status=status)

    def request_data(self, **overrides):
        data = dict(full_name='QA Client', phone='0000000000', email='qa@example.com',
                    brand='QA', model_name='Model', budget_max=15000, year_min=2020,
                    fuel='hybrid', transmission='automatic', max_mileage=0,
                    notes='Test & diacritice: mașină', privacy_consent='on')
        data.update(overrides)
        return data

    def test_home_shows_only_latest_three_available_cars(self):
        cars = [self.make_car(name=str(i)) for i in range(5)]
        self.make_car('reserved'); self.make_car('sold')
        response = self.client.get(reverse('home'))
        self.assertEqual(list(response.context['available_cars']), list(reversed(cars[-3:])))

    def test_inventory_status_sections_and_order(self):
        available = self.make_car()
        reserved = self.make_car('reserved')
        sold = self.make_car('sold')
        response = self.client.get(reverse('inventory'))
        for key, car in [('available_cars', available), ('reserved_cars', reserved), ('sold_cars', sold)]:
            self.assertEqual(list(response.context[key]), [car])
        html = response.content.decode()
        self.assertLess(html.index('id="disponibile"'), html.index('id="rezervate"'))
        self.assertLess(html.index('id="rezervate"'), html.index('id="vandute"'))

    def test_sold_car_has_no_purchase_controls(self):
        car = self.make_car('sold')
        response = self.client.get(reverse('car_detail', args=[car.pk]))
        self.assertNotContains(response, 'id="callButton"')
        self.assertNotContains(response, 'id="whatsappButton"')
        self.assertContains(response, 'Această mașină nu mai este disponibilă')

    def test_request_redirect_preserves_all_fields_including_zero_mileage(self):
        response = self.client.post(reverse('find_car'), self.request_data())
        self.assertEqual(response.status_code, 302)
        url = urlparse(response.url)
        self.assertEqual((url.scheme, url.netloc, url.path), ('https', 'wa.me', '/40757337253'))
        message = parse_qs(url.query)['text'][0]
        for value in ['QA Client', '0000000000', 'qa@example.com', 'QA', 'Model',
                      '15000 €', '2020', 'Hibrid', 'Automată',
                      'Kilometraj maxim: 0 km', 'Test & diacritice: mașină']:
            self.assertIn(value, message)
        self.assertEqual(CustomCarRequest.objects.count(), 1)

    def test_request_unspecified_mileage(self):
        response = self.client.post(reverse('find_car'), self.request_data(max_mileage=''))
        self.assertIn('Kilometraj maxim: Nespecificat', parse_qs(urlparse(response.url).query)['text'][0])

    def test_invalid_request_is_not_saved(self):
        for changes in [{'privacy_consent': ''}, {'budget_max': 0}, {'phone': '123'}, {'year_min': 1900}]:
            response = self.client.post(reverse('find_car'), self.request_data(**changes))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(response.context['form'].errors)
        self.assertEqual(CustomCarRequest.objects.count(), 0)

    def test_review_requires_consent_and_approval(self):
        data = dict(customer_name='QA Reviewer', rating=5, comment='Unique QA comment', approved='on')
        response = self.client.post(reverse('reviews'), data)
        self.assertEqual(Review.objects.count(), 0)
        data['publish_consent'] = 'on'
        response = self.client.post(reverse('reviews'), data)
        self.assertEqual(response.status_code, 302)
        review = Review.objects.get()
        self.assertFalse(review.approved)
        self.assertNotContains(self.client.get(reverse('reviews')), 'Unique QA comment')
        review.approved = True; review.save()
        self.assertContains(self.client.get(reverse('reviews')), 'Unique QA comment')

    def test_missing_car_is_404(self):
        self.assertEqual(self.client.get(reverse('car_detail', args=[999999])).status_code, 404)
