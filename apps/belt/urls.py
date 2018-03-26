from django.conf.urls import url
from . import views           
urlpatterns = [
  ## LOGIN AND REGISTRATION ROUTES
  url(r'^process$', views.process),
  url(r'^create$', views.create),
  ## ADDING/DELETING DATA
  url(r'^destroy$', views.destroy),
  url(r'^wished_items/add_item$', views.add_item),
  url(r'^remove$', views.remove),
  ## PAGE ROUTES
  url(r'^$', views.index), 
  url(r'^dashboard$', views.dashboard),
  url(r'^wished_items/create$', views.wished),
  url(r'^wished_items/[0-9]', views.item),
  url(r'^logout$', views.logout)
]