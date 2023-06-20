# import path
from django.urls import path
# import views file
# from app_name import views
from Project import views
# for password reset built-in views, import
from django.contrib.auth import views as auth_views

# define urlpattern list
urlpatterns = [
    # set the path
    # path('url', views.functionname),
    path('signup', views.signup, name='signup'),
    path('', views.signin, name='signin'),
    path('userhome',views.userhome,name='userhome'),
    path('userpage2',views.userpage2,name='userpage2'),
    path('signout',views.signout_user,name='signout'),
    # creating paths for opening views related to password reset
    path('password_reset' , auth_views.PasswordResetView.as_view(template_name='Project/password_reset.html'), name="password_reset"),
    path('password_reset_done' , auth_views.PasswordResetDoneView.as_view(template_name='Project/password_reset_done.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/' ,auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password_reset_complete' , auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]