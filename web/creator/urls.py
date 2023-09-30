from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start', views.index, name='index'),
    path('preview', views.preview),
    path('month', views.month),
    path('options', views.options),
    path('create', views.create),
    path('impressum', views.impressum),
    path('faq', views.faq)
]
