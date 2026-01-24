from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Property Management
    path('add-property/', views.add_property_view, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property_view, name='edit_property'),
    path('add-photos/<int:id>/', views.add_photos_view, name='add_photos'),
    path('manage-property/<int:id>/', views.manage_property_view, name='manage_property'),
    
    # Payment
    path('payment/<int:id>/', views.payment_view, name='payment'),
    path('verify-payment/', views.verify_payment_view, name='verify_payment'),

    # Admin
    path('admin-approve/<int:id>/', views.approve_property_view, name='approve_property'),
    path('admin-reject/<int:id>/', views.reject_property_view, name='reject_property'),
]