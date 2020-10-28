import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from ..models import PoolTarget, Target

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = 'testuser'
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password('test123')
        self.save()

class TargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PoolTarget
    
    category = 'OTHER'
    feedback_img = factory.django.ImageField(color='blue')
    feedback_img_phash = 'aaaaaaaaaaaaaaaa'
    feedback_img_chash = 'aaaaaaaaaaaaaaaa'
    tasking = 'test'
    target_description = 'test'
    active = True

class AssignedTargetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Target
    