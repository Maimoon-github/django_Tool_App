from django.test import TestCase
from django.urls import reverse
from datetime import date, timedelta

class AgeCalculatorViewTests(TestCase):
    def test_age_calculator_get(self):
        response = self.client.get(reverse('age_calculator'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Age Calculator')

    def test_age_calculator_post_valid(self):
        birth_date = (date.today() - timedelta(days=365*25 + 30)).isoformat()  # 25 years, 30 days ago
        response = self.client.post(reverse('age_calculator'), {'birth_date': birth_date})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Age Calculation Results')
        self.assertIn('age_result', response.context)
        self.assertEqual(response.context['age_result']['years'], 25)

    def test_age_calculator_post_future_date(self):
        future_date = (date.today() + timedelta(days=1)).isoformat()
        response = self.client.post(reverse('age_calculator'), {'birth_date': future_date})
        self.assertContains(response, 'Birth date cannot be in the future.')

    def test_age_calculator_post_too_old(self):
        old_date = '1899-12-31'
        response = self.client.post(reverse('age_calculator'), {'birth_date': old_date})
        self.assertContains(response, 'Birth date cannot be before 1900.')
