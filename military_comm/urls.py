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
    # Admin
    path('admin/', admin.site.urls),
    
    # Main dashboard homepage
    path('', include('dashboard.urls')),
    
    # Web UI endpoints
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard_web')),
    path('users/', include(('users.urls', 'users'), namespace='users_web')),
    path('messaging/', include(('messaging.urls', 'messaging'), namespace='messaging_web')),
    path('p2p_sync/', include(('p2p_sync.urls', 'p2p_sync'), namespace='p2p_web')),
    path('blockchain/', include(('blockchain.urls', 'blockchain'), namespace='blockchain_web')),
    path('ai_anomaly/', include(('ai_anomaly.urls', 'ai_anomaly'), namespace='ai_web')),
    
    # API endpoints
    path('api/v1/users/', include(('users.urls', 'users'), namespace='users_api')),
    path('api/v1/messaging/', include(('messaging.urls', 'messaging'), namespace='messaging_api')),
    path('api/v1/p2p-sync/', include(('p2p_sync.urls', 'p2p_sync'), namespace='p2p_api')),
    path('api/v1/blockchain/', include(('blockchain.urls', 'blockchain'), namespace='blockchain_api')),
    path('api/v1/ai-anomaly/', include(('ai_anomaly.urls', 'ai_anomaly'), namespace='ai_api')),
    path('api/v1/dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard_api')),
    
    # GraphQL
    path('graphql/', GraphQLView.as_view(graphiql=True)),
]
