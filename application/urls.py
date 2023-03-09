"""application URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from credit_card.views import CreditCardView, HolderView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('credit-cards/', CreditCardView.as_view(), name='credit-card-list'),
    path('credit-cards/<int:pk>/', CreditCardView.as_view(), name='credit-card-detail'),
    path('holders/', HolderView.as_view()),
    path('holders/<int:pk>/', HolderView.as_view()),
]
