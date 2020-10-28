from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

from PIL import Image
from captcha.client import RecaptchaResponse
from unittest.mock import patch

from . import factories
from ..models import Target

#from: http://blog.cynthiakiser.com/blog/2016/06/26/testing-file-uploads-in-django/
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='JPEG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

class TestPracticeViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.practice_url = reverse('pool:index')

    def test_anonymous_user_cant_get_target(self):
        response = self.client.post(self.practice_url, {'event':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + self.practice_url)
    
    def test_logged_user_can_get_target(self):
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'event':True})
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

class TestContributeViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.contribute_url = reverse('pool:contribute')

    def test_anonymous_user_cant_access_contribute(self):
        response = self.client.get(self.contribute_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + self.contribute_url)
    
    def test_logged_user_can_access_contribute(self):
        self.client.login(username=self.user.username, password='test123')
        response = self.client.get(self.contribute_url)
        self.assertEqual(response.status_code, 200)

    @patch("captcha.fields.client.submit")
    def test_user_can_contribute(self, mocked_submit):
        self.client.login(username=self.user.username, password='test123')
        feedback_img = create_image(None, 'feedback.jpg')
        feedback_file = SimpleUploadedFile('feedback.jpg', feedback_img.getvalue())
        mocked_submit.return_value = RecaptchaResponse(is_valid=True)
        response = self.client.post(self.contribute_url,
         {'category': 'OTHER',
          'target_description': 'This is a test',
          'tasking': 'This is a test',
          'feedback_image': feedback_file,
          'g-recaptcha-response': 'PASSED'},
           follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/pool/thanks/')
    