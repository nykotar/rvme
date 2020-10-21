from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required, permission_required
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.exceptions import ValidationError

from django.template.defaulttags import register

from pool.forms import UploadTargetForm, GetTargetForm, TargetRejectForm
from pool.models import PoolTarget, Target, Submission
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View

from .utils import gen_tid

from random import randint
import imagehash
from PIL import Image
import io
import uuid

# Create your views here.

class GetTargetView(LoginRequiredMixin, FormView):
    template_name = 'home.html'
    form_class = GetTargetForm
    success_url = '/pool/target/'

    def form_valid(self, form):
        if not form.cleaned_data['precognitive']:
            all_pooltargets = PoolTarget.objects.filter(category__in=form.cleaned_data['selected_categories'], active=True)
            done_targets = Target.objects.filter(pool_target__category__in=form.cleaned_data['selected_categories'], user=self.request.user).values_list('pool_target', flat=True)
            available_targets = all_pooltargets.exclude(pk__in=done_targets)
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
                target.pool_target = sel_target
                target.is_precog = False
                target.allowed_categories = ','.join(form.cleaned_data['selected_categories'])
                target.save()

                self.success_url += tid
            else:
                form.add_error(None, ValidationError('There are no more available targets for the selected categories.'))
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
            target.is_precog = True
            target.allowed_categories = ','.join(form.cleaned_data['selected_categories'])   
            target.save()

            self.success_url += tid

        return super(GetTargetView, self).form_valid(form)

@login_required
def target_detail(request, tid):
    target = get_object_or_404(Target, target_id=tid, user=request.user)
    return render(request, 'target_detail.html', {'target':target})

@login_required
def reveal_target(request, tid):

    target = get_object_or_404(Target, target_id=tid, user=request.user)

    if target.is_precog:
        available_targets = PoolTarget.objects.filter(category__in=target.allowed_categories.split(','), active=True)
        count = available_targets.count()
        sel_target = available_targets[randint(0, count - 1)]
        target.pool_target = sel_target

    target.revealed = True
    target.reveal_date = now()
    target.save()

    return HttpResponseRedirect(reverse('pool:target_detail', kwargs={'tid': tid}))

class UploadTargetView(LoginRequiredMixin, FormView):

    template_name = 'upload_target.html'
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
            submission.category = form.cleaned_data['category']
            submission.description = form.cleaned_data['description']
            submission.save()
            

            upload = PoolTarget()
            upload.category = form.cleaned_data['category']
            upload.description = form.cleaned_data['description']
            upload.feedback_img = form.cleaned_data['feedback_image']
            upload.feedback_img_chash = imagehash.colorhash(image)
            upload.feedback_img_phash = phash
            upload.submission = submission
            upload.save()
        '''
        else:
            form.add_error(None, ValidationError('Thank you, but this image appears to be already in our.'))
            return self.form_invalid(form)
        '''

        return super(UploadTargetView, self).form_valid(form)


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

@register.filter
def get_range(value):
    return range(1, value + 1)