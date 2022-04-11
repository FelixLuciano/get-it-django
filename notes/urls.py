from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('notes', views.notes_view, name='notes'),
    path('tags', views.tags_view, name='all tags'),
    path('t/<str:tag>', views.tag_view, name='tags'),
]
