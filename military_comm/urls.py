"""
URL configuration for military_comm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dashboard.urls')),  # Main dashboard homepage
    path('users/', include('users.urls')),
    path('messaging/', include('messaging.urls')),
    path('p2p_sync/', include('p2p_sync.urls')),
    path('blockchain/', include('blockchain.urls')),
    path('ai_anomaly/', include('ai_anomaly.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/users/', include('users.urls')),
    path('api/messaging/', include('messaging.urls')),
    path('api/p2p_sync/', include('p2p_sync.urls')),
    path('api/blockchain/', include('blockchain.urls')),
    path('api/ai_anomaly/', include('ai_anomaly.urls')),
    path('api/dashboard/', include('dashboard.urls')),
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
