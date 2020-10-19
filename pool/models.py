from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Submission(models.Model):
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploader')
    submission_date = models.DateTimeField(auto_now=True)
    moderated = models.BooleanField(default=False)
    moderated_date = models.DateTimeField(blank=True, null=True)
    moderated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='moderator')
    approved = models.BooleanField(default=False)
    rejection_reason = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=12, null=False, blank=False)
    description = models.TextField()

    class Meta:
        ordering = ['submission_date']

class PoolTarget(models.Model):

    category = models.CharField(max_length=12, null=False, blank=False)
    feedback_img = models.ImageField()
    feedback_img_phash = models.CharField(max_length=16, unique=True)
    feedback_img_chash = models.CharField(max_length=16)
    description = models.TextField()
    active = models.BooleanField(default=False)
    submission = models.OneToOneField(Submission, on_delete=models.CASCADE, null=True)

class Target(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    target_id = models.CharField(max_length=9)
    pool_target = models.ForeignKey(PoolTarget, on_delete=models.CASCADE, null=True)
    revealed = models.BooleanField(default=False)
    reveal_date = models.DateTimeField(blank=True, null=True)
    is_precog = models.BooleanField()
    allowed_categories = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.target_id

    class Meta:
        ordering = ['-created']