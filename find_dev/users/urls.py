from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', views.login_user, name='login_user'),
    path('logout/', views.logout_user, name='logout_user'),
    path('register/', views.register_user, name='register_user'),

    path('password/reset/', auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'),
         name='password_reset'),
    path('password/reset/sent/',
         auth_views.PasswordResetDoneView.as_view(template_name='users/reset_password_sent.html'),
         name='password_reset_done'),
    path('password/reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_password_confirm.html'),
         name='password_reset_confirm'),
    path('password/reset/complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/reset_password_complete.html'),
         name='password_reset_complete'),

    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>', views.user_profile, name='user_profile'),
    path('account/', views.user_account, name='user_account'),
    path('edit_account/', views.edit_account, name='edit_account'),

    path('create_skill/', views.create_skill, name='create_skill'),
    path('update_skill/<str:pk>', views.update_skill, name='update_skill'),
    path('delete_skill/<str:pk>', views.delete_skill, name='delete_skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<str:pk>', views.message_view, name='message'),
    path('create-message/<str:pk>', views.create_message, name='create_message'),
]
