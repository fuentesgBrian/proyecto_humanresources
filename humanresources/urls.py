from django.urls import path

from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('filtroslista/', views.filter_view, name='filter'),
    path('employee_search/', views.employee_search, name='employee_search'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout')
]
