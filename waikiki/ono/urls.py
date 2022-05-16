from django.urls import path

from . import views

app_name = 'ono'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/collection/', views.collection, name="collection"),
    path('<int:user_id>/mint/', views.mint, name="mint"),
    path('test/minting/', views.test_minting, name="test_minting"),
]