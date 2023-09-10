from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class Loan(models.Model):
    uuid = models.UUIDField()
    loan_type_id = models.PositiveIntegerField()
    loan_amount = models.PositiveIntegerField()
    interest_rate = models.FloatField()
    term_period = models.PositiveIntegerField()
    disbursement_date = models.DateField()
    is_active = models.BooleanField(null=True)
    remaining_amount = models.PositiveIntegerField(null=True)
    remaining_period = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class LoanType(models.Model):
    loan_type = models.CharField(max_length=25)
    max_approved_amount = models.PositiveIntegerField()


class Transaction(models.Model):
    loan = models.PositiveIntegerField()
    amount_paid = models.PositiveIntegerField()
    date = models.DateField()
    remaining_amount = models.PositiveIntegerField(null=True)
    remaining_period = models.PositiveIntegerField(null=True)



