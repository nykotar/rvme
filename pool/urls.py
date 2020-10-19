from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'pool'
urlpatterns = [
    path('', views.GetTargetView.as_view(), name='index'),
    path('contribute/', views.UploadTargetView.as_view(), name='contribute'),
    path('thanks/', TemplateView.as_view(template_name='thanks.html'), name='thanks'),
    path('viewedTargets/', views.ViewedTargetsListView.as_view(), name='viewed_targets'),
    path('viewedTargets/reset/', views.ResetViewedTargets.as_view(), name='reset_viewed_targets'),
    path('approvalQueue/', views.PoolTargetQueueListView.as_view(), name='approval_queue'),
    path('approvalQueue/<int:pk>/detail/', views.TargetDetailApproval.as_view(), name='target_detail_approval'),
    path('approvalQueue/<int:pk>/approve/', views.approve_target, name='approve_target'),
    path('approvalQueue/<int:pk>/reject/', views.RejectTarget.as_view(), name='reject_target'),
    path('moderatedList/', views.PoolTargetModeratedListView.as_view(), name='moderated_submissions'),
    path('target/<str:tid>/', views.target_detail, name='target_detail'),
    path('target/<str:tid>/reveal/', views.reveal_target, name='reveal_target')
]