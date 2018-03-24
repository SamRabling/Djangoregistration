from django.conf.urls import url
from . import views           
urlpatterns = [
  url(r'^$', views.index), 
  url(r'^process$', views.process),
  url(r'^success$', views.success),
  url(r'^create$', views.create),
  url(r'^update$', views.update),
  url(r'^loggout$', views.loggout),
  url(r'^destroy$', views.destroy)
]