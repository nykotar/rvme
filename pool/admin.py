from django.contrib import admin

# Register your models here.
from .models import Target, PoolTarget, Submission

@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):

    list_display = ('description', 'submitted_by', 'submission_date', 'moderated', 'approved')
    list_filter = ('moderated', 'approved')
    readonly_fields = ('submitted_by', 'submission_date', 'moderated_by', 'moderated_date', 'image_tag')

    fieldsets = (
        (None, {
            'fields': ('image_tag', 'category', 'description', 'submitted_by', 'submission_date')
        }),
        ('Moderation', {
            'fields': ('moderated_date', 'moderated_by', 'rejection_reason', 'approved')
        })
    )

admin.site.register(Target)
admin.site.register(PoolTarget)