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
    path('target/<str:tid>/', views.target_detail, name='target_detail'),
    path('target/<str:tid>/reveal/', views.reveal_target, name='reveal_target'),
    path('shared/target/<str:uuid>/', views.target_detail_public, name='shared_target_detail'),
    path('personalTargets/', views.PersonalTargetsView.as_view(), name="personal_targets"),
    path('personalTargets/new/', views.NewPersonalTargetView.as_view(), name="new_personal_target"),
    path('personalTarget/<str:tid>/', views.personal_target_detail, name='personal_target_detail'),
    path('personalTarget/<str:tid>/reveal/', views.reveal_personal_target, name='reveal_personal_target'),
    path('personalTarget/<str:tid>/conclude/', views.conclude_personal_target, name='conclude_personal_target'),
    path('personalTarget/<str:tid>/return/', views.return_personal_target, name='return_personal_target'),
]