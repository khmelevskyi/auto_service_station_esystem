"""
URL configuration for ServiceStation project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from website_app import views

from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView

urlpatterns = [  
    path('admin/', admin.site.urls),
    path('', views.main),
    path('show/<table_name_arg>',views.show),
    path('create/<table_name_arg>', views.create),  
    path('edit/<table_name_arg>/<id>', views.edit),
    path('delete/<table_name_arg>/<id>', views.destroy),

    path('api/<table_name_arg>', views.show_api),
    path('api/<table_name_arg>/<id>', views.show_api),

    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True)))
]  