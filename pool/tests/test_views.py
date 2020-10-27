from django.conf import settings
from django.test import TestCase
from django.urls import reverse

from . import factories
from ..models import Target

class TestPracticeViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.practice_url = reverse('pool:index')

    def test_anonymous_user_cant_get_target(self):
        practice_url = reverse('pool:index')
        response = self.client.post(practice_url, {'event':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + practice_url)
    
    def test_logged_user_can_get_target(self):
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'event':True}, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_can_get_and_reveal_target(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'other':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        reveal_url = reverse('pool:reveal_target', kwargs={'tid': target_id})
        response = self.client.get(reveal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertTrue(target.revealed)
    
    def test_can_get_and_reveal_precog_target(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'other':True, 'precognitive':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertIsNone(target.pool_target, msg='A pooltarget was assigned to a precognitive target ahead of time!')
        reveal_url = reverse('pool:reveal_target', kwargs={'tid': target_id})
        response = self.client.get(reveal_url, follow=True)
        self.assertEqual(response.status_code, 200)
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertTrue(target.revealed)

    def test_can_access_target_public_url(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'other':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        target = Target.objects.get(user=self.user, target_id=target_id)
        response = self.client.get(reverse('pool:shared_target_detail', kwargs={'uuid':target.target_uid}))
        self.assertEqual(response.status_code, 200)