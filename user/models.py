from django.db import models
from django.contrib.auth.models import User

class TokenReset(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    resettoken = models.CharField(max_length=300, blank=True, null=True)

    # def __str__(self):
    #     return self.resettoken
