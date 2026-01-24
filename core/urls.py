from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add-property/', views.add_property_view, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property_view, name='edit_property'),
    path('add-photos/<int:id>/', views.add_photos_view, name='add_photos'),
    path('payment/<int:id>/', views.payment_view, name='payment'),
    path('process-payment/<int:id>/', views.process_payment_view, name='process_payment'),
]