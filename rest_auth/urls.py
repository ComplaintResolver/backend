from rest_framework.authtoken import views as authviews

from django.conf.urls import url

from . import views

urlpatterns = [

    url(r'^login/$', authviews.obtain_auth_token),
    url(r'^change_password/$', views.change_password),
    url(r'^forgot_password/$', views.forgot_password),
    url(r'^forgot_password/done/$', views.forgot_password_done),

]
