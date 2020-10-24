from django.contrib.auth.forms import UserCreationForm
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class RecaptchaUserCreationForm(UserCreationForm):

    recaptcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)