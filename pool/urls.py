from django.urls import path

from . import views

app_name = 'pool'
urlpatterns = [
    path('', views.GetTargetView.as_view(), name='index'),
    path('contribute/', views.UploadTargetView.as_view(), name='contribute'),
    path('thanks/', views.ThanksTemplateView.as_view(), name='thanks'),
    path('viewedTargets/', views.ViewedTargetsListView.as_view(), name='viewed_targets'),
    path('viewedTargets/reset/', views.ResetViewedTargets.as_view(), name='reset_viewed_targets'),
    path('target/<str:tid>/', views.target_detail, name='target_detail'),
    path('target/<str:tid>/reveal/', views.RevealTargetView.as_view(), name='reveal_target'),
    path('shared/target/<str:uuid>/', views.target_detail_public, name='shared_target_detail'),
    path('personalTargets/', views.PersonalTargetsView.as_view(), name="personal_targets"),
    path('personalTargets/new/', views.NewPersonalTargetView.as_view(), name="new_personal_target"),
    path('personalTarget/<str:tid>/', views.personal_target_detail, name='personal_target_detail'),
    path('personalTarget/<str:tid>/reveal/', views.RevealPersonalTargetView.as_view(), name='reveal_personal_target'),
    path('personalTarget/<str:tid>/conclude/', views.ConcludePersonalTargetView.as_view(), name='conclude_personal_target'),
    path('personalTarget/<str:tid>/return/', views.ReturnPersonalTargetView.as_view(), name='return_personal_target'),
    path('settings/', views.SettingsTemplateView.as_view(), name="user_settings"),
    path('settings/changePassword/', views.ChangePasswordView.as_view(), name="change_password")
]