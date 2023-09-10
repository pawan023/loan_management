from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Create your models here.

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    aadhar_id = models.CharField(max_length=50)
    annual_income = models.PositiveIntegerField(null=True)
    credit_score = models.PositiveIntegerField(null=True)
