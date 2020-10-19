from django.http import HttpResponse
from django.views.generic.edit import FormView
from django.contrib.auth import login, authenticate

from django.contrib.auth.forms import UserCreationForm

class SignupView(FormView):

    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/pool/'

    def form_valid(self, form):
        form.save()
        user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))
        login(self.request, user)
        return super(SignupView, self).form_valid(form)