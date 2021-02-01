from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

from django.template.defaulttags import register

from pool.forms import UploadTargetForm, GetTargetForm, NewPersonalTargetForm
from pool.models import PoolTarget, Target, Submission, PersonalTarget
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

from .utils import gen_tid, encrypt, decrypt

from random import randint
import imagehash
from PIL import Image
import io
import uuid, shortuuid
import markdown

# Create your views here.

'''
** Practice views
'''
class GetTargetView(LoginRequiredMixin, FormView):
    template_name = 'home.html'
    form_class = GetTargetForm
    success_url = '/pool/target/'

    def form_valid(self, form):
        if not form.cleaned_data['precognitive']:
            all_pooltargets = PoolTarget.objects.filter(level=form.cleaned_data['level'], active=True)
            done_targets = Target.objects.filter(pool_target__level=form.cleaned_data['level'],
                                                user=self.request.user).values_list('pool_target', flat=True)
            available_targets = all_pooltargets.exclude(pk__in=done_targets)
            if not form.cleaned_data['incsubmitted']:
                available_targets = available_targets.exclude(submission__submitted_by=self.request.user)
            count = available_targets.count()

            if count > 0:
                sel_target = available_targets[randint(0, count - 1)]
                
                tid = gen_tid()
                exists = Target.objects.filter(user=self.request.user, target_id=tid).exists()
                while exists:
                    tid = gen_tid()
                    exists = Target.objects.filter(user=self.request.user, target_id=tid).exists()

                target = Target()
                target.user = self.request.user
                target.target_id = tid
                target.target_uid = shortuuid.uuid()
                target.pool_target = sel_target
                target.is_precog = False
                target.level = form.cleaned_data['level']
                target.allowed_categories = ''
                target.save()

                self.success_url += tid
            else:
                form.add_error(None, ValidationError('There are no more available targets for you in the selected level.'))
                return self.form_invalid(form)
        else:
            tid = gen_tid()
            exists = Target.objects.filter(user=self.request.user, target_id=tid).exists()
            while exists:
                tid = gen_tid()
                exists = Target.objects.filter(user=self.request.user, target_id=tid).exists()

            target = Target()
            target.user = self.request.user
            target.target_id = tid
            target.target_uid = shortuuid.uuid()
            target.is_precog = True
            target.inc_submitted = form.cleaned_data['incsubmitted']
            target.allowed_categories = ''
            target.level = form.cleaned_data['level']  
            target.save()

            self.success_url += tid

        return super(GetTargetView, self).form_valid(form)

@login_required
def target_detail(request, tid):
    target = get_object_or_404(Target, target_id=tid, user=request.user)
    return render(request, 'target_detail.html', {'target':target})

def target_detail_public(request, uuid):
    target = get_object_or_404(Target, target_uid=uuid)
    return render(request, 'target_detail.html', {'target':target})

class RevealTargetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tid = kwargs['tid']
        target = get_object_or_404(Target, target_id=tid, user=request.user)

        if target.is_precog:
            available_targets_ = PoolTarget.objects.filter(level=target.level, active=True)
            if not target.inc_submitted:
                available_targets_ = available_targets_.exclude(submission__submitted_by=request.user)
            done_targets = Target.objects.filter(pool_target__level=target.level,
                                                user=self.request.user).values_list('pool_target', flat=True)
            available_targets = available_targets_.exclude(pk__in=done_targets)
            count = available_targets.count()
            if count == 0:
                available_targets = available_targets_
                count = available_targets.count()
            sel_target = available_targets[randint(0, count - 1)]
            target.pool_target = sel_target

        target.revealed = True
        target.reveal_date = now()
        target.save()

        return HttpResponseRedirect(reverse('pool:target_detail', kwargs={'tid': tid}))

'''
** Contribute views
'''
class UploadTargetView(LoginRequiredMixin, FormView):

    template_name = 'contribute.html'
    form_class = UploadTargetForm
    success_url = '/pool/thanks/'

    def form_valid(self, form):
        
        image = Image.open(form.cleaned_data['feedback_image'])
        # Downscale image
        image.thumbnail(settings.IMAGE_MAX_SIZE, Image.ANTIALIAS)
        phash = imagehash.phash(image)
        if not PoolTarget.objects.filter(feedback_img_phash=phash).exists():
            
            # Fix PNG
            if image.format == 'PNG':
                image = image.convert('RGB')

            image_io = io.BytesIO()
            image.save(image_io, format='JPEG')
            file = InMemoryUploadedFile(
                image_io, 'feedback_image',
                f'{uuid.uuid4().hex}.jpg',
                'image/jpeg',
                None, None
            )
            form.cleaned_data['feedback_image'] = file

            submission = Submission()
            submission.submitted_by = self.request.user
            submission.level = form.cleaned_data['level']
            submission.target_description = form.cleaned_data['target_description']
            submission.tasking = form.cleaned_data['tasking']
            if form.cleaned_data['additional_feedback']:
                submission.additional_feedback = form.cleaned_data['additional_feedback']
            submission.save()
            

            upload = PoolTarget()
            upload.level = form.cleaned_data['level']
            upload.target_description = form.cleaned_data['target_description']
            upload.tasking = form.cleaned_data['tasking']
            if form.cleaned_data['additional_feedback']:
                upload.additional_feedback = form.cleaned_data['additional_feedback']
            upload.feedback_img = form.cleaned_data['feedback_image']
            upload.feedback_img_phash = phash
            upload.submission = submission
            upload.save()
        '''
        else:
            form.add_error(None, ValidationError('Thank you, but this image appears to be already in our database.'))
            return self.form_invalid(form)
        '''

        return super(UploadTargetView, self).form_valid(form)

class ThanksTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'thanks.html'

'''
** Viewed targets views
'''
class ViewedTargetsListView(LoginRequiredMixin, ListView):

    model = Target
    context_object_name = 'targets'
    paginate_by = 10
    template_name = 'viewed_targets.html'

    def get_queryset(self):
        queryset = Target.objects.filter(user=self.request.user)
        return queryset

class ResetViewedTargets(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        Target.objects.filter(user=request.user).delete()
        return HttpResponseRedirect(reverse('pool:viewed_targets'))

'''
** Personal Targets
'''
class PersonalTargetsView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        target_count = PersonalTarget.objects.filter(user=request.user).count()
        try:
            current = PersonalTarget.objects.filter(user=request.user, active=True).get()
        except PersonalTarget.DoesNotExist:
            current = None
        return render(request, 'personal_targets.html', context={'target_count': target_count, 'current':current})

    def post(self, request, *args, **kwargs):
        target_count = PersonalTarget.objects.filter(user=request.user).count()
        if target_count:
            available = PersonalTarget.objects.filter(user=request.user).all()
            selected = available[randint(0, target_count - 1)]
            selected.active = True
            selected.tid = gen_tid()
            selected.save()
            return HttpResponseRedirect(reverse('pool:personal_target_detail', kwargs={'tid':selected.tid}))
        else:
            return HttpResponseRedirect(reverse('pool:personal_targets'))

class NewPersonalTargetView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = NewPersonalTargetForm(request.POST)
        if form.is_valid():
            personal_target = PersonalTarget()
            personal_target.user = request.user
            html = markdown.markdown(form.cleaned_data['tasking'], extensions=['sane_lists'])
            personal_target.tasking = encrypt(html)
            personal_target.save()
        return HttpResponseRedirect(reverse('pool:personal_targets'))

@login_required
def personal_target_detail(request, tid):
    target = get_object_or_404(PersonalTarget, tid=tid, user=request.user)
    return render(request, 'personal_target_detail.html', {'target':target})

class RevealPersonalTargetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tid = kwargs['tid']
        target = get_object_or_404(PersonalTarget, tid=tid, user=request.user)
        target.revealed = True
        target.save()
        return HttpResponseRedirect(reverse('pool:personal_target_detail', kwargs={'tid':tid}))

class ConcludePersonalTargetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tid = kwargs['tid']
        target = get_object_or_404(PersonalTarget, tid=tid, user=request.user)
        target.delete()
        messages.success(request, 'The target was concluded and removed from the pool.')
        return HttpResponseRedirect(reverse('pool:personal_targets'))

class ReturnPersonalTargetView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        tid = kwargs['tid']
        target = get_object_or_404(PersonalTarget, tid=tid, user=request.user)
        target.active = False
        target.revealed = False
        target.save()
        messages.success(request, 'The target was returned to the pool.')
        return HttpResponseRedirect(reverse('pool:personal_targets'))

@register.filter
def get_range(value):
    return range(1, value + 1)

@register.filter
def decryptTxt(value):
    return decrypt(value)

'''
** Settings
'''

class SettingsTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'settings.html'

class ChangePasswordView(LoginRequiredMixin, View):

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return HttpResponseRedirect(reverse('pool:user_settings'))
        else:
            messages.error(request, 'Please correct the error below.')
            return render(request, template_name='settings.html', context={'form':form})