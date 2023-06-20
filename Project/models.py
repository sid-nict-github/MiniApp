from django.db import models
# import the User class
from django.contrib.auth.models import User

# Create your models here.
# create a model that represent the user
class UserProfileInfo(models.Model):
    # declare a foreign key object of the User
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL )
    # define additional features
    phone = models.CharField(max_length=255, null=True)
    # spl. member function __str__()
    def __str__(self):
        return self.user.username