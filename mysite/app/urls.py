from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProgrammerListView.as_view(), name='list'),
    path('model_index/<programmer_id>', views.model_index, name='model_index'),
    path('inline_index/<programmer_id>', views.inline_index, name='inline_index'),
    path('edit_user/<pk>', views.edit_user, name='edit_user'),
    path('add_user', views.add_user, name='add_user')
]