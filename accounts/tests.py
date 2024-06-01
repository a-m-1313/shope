from django.test import TestCase
from django.urls import reverse


class AccountTestClass(TestCase):

    def test_url_by_name_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_url_login_page(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_template_login_page(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'account/login.html')
        self.assertEqual(response.status_code, 200)

    def test_url_signup_page(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_template_signup_page(self):
        response = self.client.get(reverse('signup'))
        self.assertTemplateUsed(response, 'account/signup.html')
        self.assertEqual(response.status_code, 200)


