from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO

from PIL import Image
from captcha.client import RecaptchaResponse
from unittest.mock import patch

from . import factories
from ..models import Target, PersonalTarget

#from: http://blog.cynthiakiser.com/blog/2016/06/26/testing-file-uploads-in-django/
def create_image(storage, filename, size=(100, 100), image_mode='RGB', image_format='JPEG'):
    data = BytesIO()
    Image.new(image_mode, size).save(data, image_format)
    data.seek(0)
    if not storage:
        return data
    image_file = ContentFile(data.read())
    return storage.save(filename, image_file)

class TestAccounts(TestCase):

    @patch("captcha.fields.client.submit")
    def test_can_signup(self, mocked_submit):
        mocked_submit.return_value = RecaptchaResponse(is_valid=True) 
        response = self.client.post(reverse('signup'),
         {'username':'test',
          'password1':'aolswontgetme',
          'password2':'aolswontgetme',
          'g-recaptcha-response': 'PASSED'},
          follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:index'))

class TestPracticeViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()
        self.practice_url = reverse('pool:index')

    def test_anonymous_user_cant_get_target(self):
        response = self.client.post(self.practice_url, {'level':'BEGINNER'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + self.practice_url)
    
    def test_logged_user_can_get_target(self):
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'level':'BEGINNER'})
        self.assertEqual(response.status_code, 200)

    def test_can_get_and_reveal_target(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'level':'BEGINNER'}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        reveal_url = reverse('pool:reveal_target', kwargs={'tid': target_id})
        response = self.client.post(reveal_url, {}, follow=True)
        self.assertEqual(response.status_code, 200)
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertTrue(target.revealed)
    
    def test_can_get_and_reveal_precog_target(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'level':'BEGINNER', 'precognitive':True}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertIsNone(target.pool_target, msg='A pooltarget was assigned to a precognitive target ahead of time!')
        reveal_url = reverse('pool:reveal_target', kwargs={'tid': target_id})
        response = self.client.post(reveal_url, {}, follow=True)
        self.assertEqual(response.status_code, 200)
        target = Target.objects.get(user=self.user, target_id=target_id)
        self.assertTrue(target.revealed)

    def test_can_access_target_public_url(self):
        factories.TargetFactory()
        self.client.login(username=self.user.username, password='test123')
        response = self.client.post(self.practice_url, {'level':'BEGINNER'}, follow=True)
        self.assertEqual(response.status_code, 200)
        target_id = response.redirect_chain[0][0][-9:]
        target = Target.objects.get(user=self.user, target_id=target_id)
        response = self.client.get(reverse('pool:shared_target_detail', kwargs={'uuid':target.target_uid}))
        self.assertEqual(response.status_code, 200)

    def test_anonymous_user_cant_access_viewed_targets(self):
        viewed_targets_url = reverse('pool:viewed_targets')
        response = self.client.get(viewed_targets_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + viewed_targets_url)

    def test_logged_user_can_access_viewed_targets(self):
        self.client.login(username=self.user.username, password='test123')
        viewed_targets_url = reverse('pool:viewed_targets')
        response = self.client.get(viewed_targets_url)
        self.assertEqual(response.status_code, 200)

    def test_reset_viewed_targets(self):
        self.client.login(username=self.user.username, password='test123')
        factories.Target(user=self.user,
         target_uid='uuid',
         target_id='1234-4321',
         is_precog=True,
         allowed_categories='',
         level='BEGINNER').save()
        self.assertGreater(Target.objects.filter(user=self.user).count(), 0)
        reset_viewed_targets_url = reverse('pool:reset_viewed_targets')
        response = self.client.post(reset_viewed_targets_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:viewed_targets'))
        self.assertEqual(Target.objects.filter(user=self.user).count(), 0)

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
         {'level': 'BEGINNER',
          'target_description': 'This is a test',
          'additional_feedback': 'Yes.. just a test.',
          'tasking': 'This is a test',
          'feedback_image': feedback_file,
          'g-recaptcha-response': 'PASSED'},
           follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], '/pool/thanks/')
    
class TestPersonalTargetViews(TestCase):

    def setUp(self):
        self.user = factories.UserFactory()

    def test_anonymous_user_cant_access_personal_targets(self):
        personal_targets_url = reverse('pool:personal_targets')
        response = self.client.get(personal_targets_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0],
                         settings.LOGIN_URL + '?next=' + personal_targets_url)        
    
    def test_logged_user_can_access_personal_targets(self):
        self.client.login(username=self.user.username, password='test123')
        personal_targets_url = reverse('pool:personal_targets')
        response = self.client.get(personal_targets_url)
        self.assertEqual(response.status_code, 200)    

    def test_can_create_personal_target(self):
        self.client.login(username=self.user.username, password='test123')
        new_personal_targets_url = reverse('pool:new_personal_target')
        response = self.client.post(new_personal_targets_url, {'tasking':'Test tasking.'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:personal_targets'))
        self.assertGreater(PersonalTarget.objects.filter(user=self.user).count(), 0)
        personal_target = PersonalTarget.objects.filter(user=self.user).get()
        self.assertNotEqual('Test tasking.', personal_target.tasking, 'The tasking was not encrypted!')


    def test_can_get_personal_target(self):
        self.client.login(username=self.user.username, password='test123')
        new_personal_targets_url = reverse('pool:new_personal_target')
        response = self.client.post(new_personal_targets_url, {'tasking':'Test tasking.'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:personal_targets'))
        response = self.client.post(reverse('pool:personal_targets'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.redirect_chain[0][0], r'/pool/personalTarget/*/')

    def test_can_reveal_personal_target(self):
        self.client.login(username=self.user.username, password='test123')
        factories.PersonalTarget(user=self.user,
            active=True,
            tid='1234-4321',
            tasking='Z0FBQUFBQmZtTk5ERWN0TTYyY2FPcGZHTHhCeVJuNXpCd29jZi1rZ2JmVGoweEFfck9LcFBTR1RjeDN3VUxnQU5KTjFGZzNqSUVaM3lFN2tIckRVeEZDbGxpeUFNb3pZZzNqVkk3OGdWcGpvSllwaFpjMXVyZGc9'
            ).save()
        response = self.client.post(reverse('pool:reveal_personal_target', kwargs={'tid':'1234-4321'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRegex(response.redirect_chain[0][0], r'/pool/personalTarget/*/')
        self.assertTrue(PersonalTarget.objects.filter(user=self.user).get().revealed)

    def test_can_conclude_personal_target(self):
        self.client.login(username=self.user.username, password='test123')
        factories.PersonalTarget(user=self.user,
            active=True,
            tid='1234-4321',
            tasking='Z0FBQUFBQmZtTk5ERWN0TTYyY2FPcGZHTHhCeVJuNXpCd29jZi1rZ2JmVGoweEFfck9LcFBTR1RjeDN3VUxnQU5KTjFGZzNqSUVaM3lFN2tIckRVeEZDbGxpeUFNb3pZZzNqVkk3OGdWcGpvSllwaFpjMXVyZGc9',
            revealed=True).save()
        response = self.client.get(reverse('pool:conclude_personal_target', kwargs={'tid':'1234-4321'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:personal_targets'))
        self.assertEqual(PersonalTarget.objects.count(), 0, 'Personal target was not removed from the db after conclusion!')

    def test_can_return_personal_target(self):
        self.client.login(username=self.user.username, password='test123')
        factories.PersonalTarget(user=self.user,
            active=True,
            tid='1234-4321',
            tasking='',
            revealed=True).save()
        response = self.client.get(reverse('pool:return_personal_target', kwargs={'tid':'1234-4321'}), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[0][0], reverse('pool:personal_targets'))
        self.assertEqual(PersonalTarget.objects.count(), 1)
        self.assertFalse(PersonalTarget.objects.filter(user=self.user).get().active)
        self.assertFalse(PersonalTarget.objects.filter(user=self.user).get().revealed)