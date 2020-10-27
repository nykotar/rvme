import factory
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = 'testuser'
    
    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password('test123')
        self.save()
    