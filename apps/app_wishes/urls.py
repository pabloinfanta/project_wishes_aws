
from django.urls import path

from . import views

# Create your views here.
urlpatterns = [
  path('', views.index, name='index'),
  path('form_create', views.form_create, name='form_create'),
  path('<int:id>/form_edit', views.form_edit, name='form_edit'),
  path('create_wish', views.create_wish, name='create_wish'),
  path('<int:id>/delete_wish', views.delete_wish, name='delete_wish'),
  path('<int:id>/granted_wish', views.granted_wish, name='granted_wish'),
  path('<int:id>/update_wish', views.update_wish, name='update_wish'),
  path('stats', views.stats, name='stats'),
  path('<int:id>/like', views.like, name='like'),
  #path('/<int:message_id>/create_comment', views.create_comment, name='create_comment')

]