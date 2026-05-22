# car_dealership/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('cars/<int:pk>/', views.CarDetailView.as_view(), name='car_detail'),
    path('service/', views.ServiceView.as_view(), name='service'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('test_drive/select/', views.TestDriveSelectView.as_view(), name='test_drive_select'),
    path('test-drive/book/<int:car_id>/', views.TestDriveBookView.as_view(), name='book_test_drive'),

]