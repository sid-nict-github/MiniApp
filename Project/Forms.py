# imports
from django import forms
from django.contrib.auth.models import User
from Project.models import UserProfileInfo

# define a class that represents the User form
# inherit from ModelForm
class UserForm(forms.ModelForm):
    # make the password non-readable
    password = forms.CharField(widget=forms.PasswordInput())
    # define an inner class
    class Meta:
        # specify the model
        model = User
        # specify the fields to display
        fields = ('username','password','email','first_name','last_name')


# define a class that represents additional fields of the User
class UserProfileInfoForm(forms.ModelForm):
    # define an inner class
    class Meta:
        # specify the model
        model = UserProfileInfo
        # specify the fields to display
        fields = ('phone',)