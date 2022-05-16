from django.urls import path

from . import views

app_name = 'ono'

urlpatterns = [
    path('', views.index, name='index'),
    # path('user/collection', views.collection, name="collection"),
    # path('user/mint', views.mint, name="mint"),
    # path('profile', views.profile, name="profile"),
    path('test/minting', views.test_minting, name="test_minting"),
]