from django.urls import path

from . import views

app_name = 'ono'
urlpatterns = [
    path('', views.index, name='index'),
    path('test/minting', views.test_minting, name="test_minting")
]