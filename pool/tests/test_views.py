from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from . import factories

class TestPracticeViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()

    def test_anonymous_user_cant_get_target(self):
        practice_url = reverse('pool:index')
        response = self.client.post(practice_url, {'event':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + practice_url)
    
    def test_logged_user_can_get_target(self):
        self.client.login(username=self.user.username, password='test123')
        practice_url = reverse('pool:index')
        response = self.client.post(practice_url, {'event':True}, follow=True)
        self.assertEqual(response.status_code, 200)