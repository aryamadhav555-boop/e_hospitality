from django.urls import path
from . import views
from .views import pay_bill

urlpatterns = [
    path('pay_bill/<int:bill_id>',views.pay_bill, name='pay_bill'),
    path('billing/create_bill/', views.create_bill, name='create_bill'),
    path('billing/dashboard/', views.billing_dashboard, name='billing_dashboard'),
    path('billing/success/', views.payment_success, name='payment_success'),
    path('billing/cancel/', views.payment_cancel, name='payment_cancel'),
    path('patients/dashboard/billing/list/',views.bill_list, name='bill_list'),
]


