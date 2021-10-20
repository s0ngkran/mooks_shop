"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from .views import *
from django.contrib import admin

urlpatterns = [
    # path('register/', RegisterPage.as_view(), name='register-page'),
    path('register/', LoginPage.as_view(), name='register-page'),
    path('login/', LoginPage.as_view(), name='login-page'),
    path('logout/', LogoutPage.as_view(), name='logout-page'),

    # pages
    path('', IndexPage.as_view(), name='index-page'),
    path('add-new-product/', AddNewProductPage.as_view(), name='add-new-product-page'),
    path('add-new-promotion/', PromotionCreateView.as_view(), name='add-new-promotion-page'),
    path('create-category/', CategoryCreateView.as_view(), name='create-category-page'),
    path('cashier/', CashierPage.as_view(), name='cashier-page'),
    path('transaction/', TransactionPage.as_view(), name='transaction-page'),
    path('subtransaction/<str:id>', SubTransactionPage.as_view(), name='subtransaction-page'),
    path('migrate/', MigratePage.as_view(), name='subtransaction-page'),
]
