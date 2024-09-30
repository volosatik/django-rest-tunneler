from django.urls import path
from . import views
urlpatterns =[

    path('healthcheck/', views.healthcheck),
    path('', views.request_selector),
]