from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('cars/', views.CarListView.as_view(), name='car_list'),
    path('service/', views.ServiceView.as_view(), name='service'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('test_drive/select/', views.TestDriveSelectView.as_view(), name='test_drive_select'),
    path('test-drive/book/<int:car_id>/', views.TestDriveBookView.as_view(), name='book_test_drive'),
    path('test-drive/success/', TemplateView.as_view(template_name='tasks/success.html'), name='success_page'),
    path('service/success/', TemplateView.as_view(template_name='tasks/service_success_page.html'),
         name='service_success_page'),
    path('models/<str:car_name>/', views.CarDetailView.as_view(), name='car_detail'),
    path('models/<str:car_name>/constructor/', views.car_constructor_view, name='car_constructor'),
    path('models-overview/', views.ModelsOverviewView.as_view(), name='models_overview'),
    path('service-info/', views.ServiceInfoView.as_view(), name='service_info'),
    path('special-offers/', views.SpecialOffersView.as_view(), name='special_offers'),
    path('trade-in/', views.TradeInView.as_view(), name='trade_in'),
    path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    path('contacts/', views.ContactView.as_view(), name='contacts'),

]