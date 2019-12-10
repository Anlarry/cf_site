from django.contrib.auth.models import User
from django.contrib.auth import authenticate

def Create_new_user(username, password, email=""):
    try:
        user = User.objects.get(username=username)
        return False
    except User.DoesNotExist:
        user = User.objects.create_user(username,email, password)
        user.save()
        return True

def Check_user(username, password):
    user = authenticate(username=username, password=password)
    if user is not None:
        return True
    else:
        return False



