from django.urls import path

from . import views

app_name = 'ono'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:user_id>/dashboard/', views.dashboard, name="dashboard"),
    path('<int:user_id>/collection/', views.collection, name="collection"),
    path('<int:user_id>/mint/', views.mint, name="mint"),
    path('search/', views.search, name='search'),
    path('test/image/', views.test_image, name="test_image"),
    path('test/minting/', views.test_minting, name="test_minting"),
    path('test/makecontract/', views.make_contract, name="make_contract"),
    path('test/maketoken/', views.make_token, name="make_token")

]