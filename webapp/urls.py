from django.urls import path, re_path
from . import views

urlpatterns = [
	re_path(r'^$', views.home, name='index'),
	re_path(r'^login$', views.login_view, name='login'),
	re_path(r'^logout$', views.logout_view, name='logout'),
	re_path(r'^signup$', views.signup, name='signup'),
]
