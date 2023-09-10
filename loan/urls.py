from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt

from loan.views import *

urlpatterns = [
    path('api/apply-loan/', csrf_exempt(InitiateLoan.as_view()), name='apply_loan'),
    path('api/make-payment/', csrf_exempt(EmiPayment.as_view()), name='pay_loan_emi'),
    path('api/get-statement/', csrf_exempt(GetStatement.as_view()), name='get_emi_statement'),

]
