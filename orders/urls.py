from django.urls import path
from . import views 


app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('created/', views.order_created_view, name='created'),
    path('admin/order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
]
