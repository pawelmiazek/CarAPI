from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('', views.api_overview, name='api-overview'),
    path('cars/', views.CarListCreate.as_view(), name='car-list-create'),
    path('rate/', views.RateCreate.as_view(), name='rate-create'),
    path('popular/', views.PopularView.as_view(), name='popular-list'),
]
