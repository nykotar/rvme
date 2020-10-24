from django.contrib import admin
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.contrib import messages

# Register your models here.
from .models import Target, PoolTarget, Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    change_form_template = 'admin/submission_changeform.html'

    list_filter = ('moderated', 'approved', 'category')
    list_display = ('target_description', 'category','submitted_by', 'submission_date', 'status')
    search_fields = ('target_description', 'additional_feedback', 'submitted_by__username')
    readonly_fields = ('submitted_by', 'submission_date', 'moderated_by', 'moderated_date', 'image_tag', 'status')

    fieldsets = (
        (None, {
            'fields': ('image_tag', 'category', 'target_description', 'tasking', 'additional_feedback', 'submitted_by', 'submission_date')
        }),
        ('Moderation', {
            'fields': ('status', 'moderated_date', 'moderated_by', 'rejection_reason')
        })
    )

    def response_change(self, request, obj):
        if '_approve' in request.POST:
            obj.moderated = True
            obj.moderated_by = request.user
            obj.moderated_date = now()
            obj.approved = True
            obj.save()
            obj.pooltarget.active = True
            obj.pooltarget.target_description = obj.target_description
            obj.pooltarget.tasking = obj.tasking
            obj.pooltarget.additional_feedback = obj.additional_feedback
            obj.pooltarget.save()
            self.message_user(request, 'Submission approved.')
            return HttpResponseRedirect('.')
        elif '_reject' in request.POST:
            if obj.rejection_reason:
                obj.moderated = True
                obj.moderated_by = request.user
                obj.moderated_date = now()
                obj.approved = False
                obj.save()
                obj.pooltarget.delete()
                self.message_user(request, 'Submission rejected.')
            else:
                self.message_user(request, 'Please specify the rejection reason.', level=messages.ERROR)
            return HttpResponseRedirect('.')
        return super().response_change(request, obj)

@admin.register(PoolTarget)
class PoolTargetAdmin(admin.ModelAdmin):

    list_filter = ('category', 'active')
    list_display = ('target_description', 'category', 'active')
    search_fields = ('target_description', 'additional_feedback')

@admin.register(Target)
class Target(admin.ModelAdmin):

    list_filter = ('revealed', 'is_precog')
    list_display = ('target_id', 'is_precog', 'revealed', 'user', 'created')
    search_fields = ('target_id', 'user__username')