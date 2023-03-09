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
from django.urls import path, include
from credit_card.views import CreditCardView, HolderView, UserCreateView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework import routers
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Credit Card API",
        default_version='v1',
        description="This is a simple swagger of routes of all endpoints available for this project.",
        contact=openapi.Contact(email="luiz.gustavo.silva1@outlook.com"),
        license=openapi.License(name="Puzzle Solutions LTDA"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credit-cards/', CreditCardView.as_view(), name='credit-card-list'),
    path('credit-cards/<int:pk>/', CreditCardView.as_view(), name='credit-card-detail'),
    path('holders/', HolderView.as_view(), name='holder-list'),
    path('holders/<int:pk>/', HolderView.as_view(), name='holder-detail'),
    path('sign-up/', UserCreateView.as_view(), name='user-create'),
    path('api/token/', obtain_auth_token, name='api_token_auth'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
