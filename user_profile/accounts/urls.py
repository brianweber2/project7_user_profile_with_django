from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'sign_in/$', views.sign_in, name='sign_in'),
    url(r'sign_up/$', views.sign_up, name='sign_up'),
    url(r'sign_out/$', views.sign_out, name='sign_out'),
    url(r'profile/$', views.user_profile, name='profile'),
    url(r'profile/edit/$', views.edit_user_profile, name='edit_profile'),
    url(r'profile/change_password/$', views.change_password, name='change_password'),
]
