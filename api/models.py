from django.db import models
from django.contrib.auth.models import User



class UserModel(User):
    last_vent = models.DateTimeField(null=True)
    score = models.IntegerField(default=0)

