from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import mark_safe

# Create your models here.
class Submission(models.Model):

    CATEGORIES = (
        ('PERSON', 'Person'),
        ('LIFEFORM', 'Lifeform'),
        ('OBJECT', 'Object'),
        ('LOCATION', 'Location'),
        ('EVENT', 'Event'),
        ('OTHER', 'Other')
    )

    LEVELS = (
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', ' Intermediate'),
        ('ADVANCED', 'Advanced')
    )

    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    submission_date = models.DateTimeField(auto_now_add=True)
    moderated = models.BooleanField(default=False)
    moderated_date = models.DateTimeField(blank=True, null=True)
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderator')
    approved = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=12, choices=CATEGORIES, null=True, blank=True)
    level = models.CharField(max_length=12, choices=LEVELS, null=False, blank=False, default='ADVANCED')
    tasking = models.TextField(null=False, blank=False)
    target_description = models.CharField(max_length=255, null=False, blank=False)
    additional_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.target_description

    def save(self, *args, **kwargs):
        if self.id:
            self.pooltarget.category = self.category
            self.pooltarget.level = self.level
            self.pooltarget.save()
        super(Submission, self).save(*args, **kwargs)

    def image_tag(self):
        src = settings.MEDIA_URL + str(self.pooltarget.feedback_img)
        return mark_safe(f'<a href="{src}" target="blank"><img src="{src}" width="350" height="300" /></a>')

    def status(self):
        if self.moderated:
            if self.approved:
                return 'Approved'
            else:
                return 'Rejected'
        else:
            return '-'
    
    image_tag.short_description = 'Feedback Image'

    class Meta:
        ordering = ['-submission_date']

class PoolTarget(models.Model):

    category = models.CharField(max_length=12, null=True, blank=True)
    level = models.CharField(max_length=12, null=False, blank=False, default='ADVANCED')
    feedback_img = models.ImageField()
    feedback_img_phash = models.CharField(max_length=16, unique=True)
    tasking = models.TextField()
    target_description = models.CharField(max_length=255)
    additional_feedback = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.target_description


class Target(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_uid = models.CharField(max_length=22, unique=True)
    target_id = models.CharField(max_length=9)
    pool_target = models.ForeignKey(PoolTarget, on_delete=models.CASCADE, null=True)
    revealed = models.BooleanField(default=False)
    reveal_date = models.DateTimeField(blank=True, null=True)
    is_precog = models.BooleanField()
    inc_submitted = models.BooleanField(default=False)
    allowed_categories = models.CharField(max_length=64)
    level = models.CharField(max_length=12, default='ADVANCED')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.target_id

    class Meta:
        ordering = ['-created']

class PersonalTarget(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tasking = models.TextField()
    tid = models.CharField(max_length=9, null=True, blank=True)
    active = models.BooleanField(default=False)
    revealed = models.BooleanField(default=False)