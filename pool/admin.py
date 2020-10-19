from django.contrib import admin

# Register your models here.
from .models import Target, PoolTarget, Submission

@admin.register(Target, PoolTarget, Submission)
class TargetAdmin(admin.ModelAdmin):
    pass