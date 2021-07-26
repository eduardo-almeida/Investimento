from django.urls import path
from . import views

urlpatterns = [
    path('coinList/', views.coinList, name='coin-list'),
    path('coin/<int:id>', views.coinView, name='coin-view'),
    path('newcoin/', views.newCoin, name='new-coin'),
    path('editcoin/<int:id>', views.editCoin, name='edit-coin'),
    path('deletecoin/<int:id>', views.deleteCoin, name='delete-coin'),
]
