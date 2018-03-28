from django.conf.urls import url
from . import views           
urlpatterns = [
  ## LOGIN AND REGISTRATION ROUTES
  url(r'^process$', views.process),
  url(r'^create$', views.create),
  ## ADDING/DELETING DATA
  url(r'^destroy$', views.destroy),
  url(r'^wished_items/add$', views.add),
  url(r'^wished_items/add_to_wishlist$', views.add_to_wishlist),
  url(r'^wished_items/add_to_my_wishlist/(?P<id>\d+)$', views.add_to_my_wishlist),
  url(r'^wished_items/unwish/(?P<id>\d+)$', views.un_wish),
  ## PAGE ROUTES
  url(r'^$', views.index), 
  url(r'^dashboard$', views.dashboard),
  url(r'^wished_items/(?P<id>\d+)$', views.item),
  url(r'^logout$', views.logout)
]