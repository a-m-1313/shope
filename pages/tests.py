from django.core.paginator import Page
from django.test import TestCase
from django.urls import reverse


class TestPages(TestCase):

    def test_url_name_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_by_urls_home_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_by_template_home_page(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_url_name_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_by_urls_about_page(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_by_template_about_page(self):
        response = self.client.get(reverse('about'))
        self.assertTemplateUsed(response, 'pages/about.html')


