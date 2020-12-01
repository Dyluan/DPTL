from django.urls import path
from . import views

app_name = 'appartements'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('login/', views.FormView.as_view(), name='login'),
]
