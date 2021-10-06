from django.db import models
from apps.app_users.models import User

# Create your models here.

class WishManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    if len(postData['item']) < 2:
      errors["item"] = "Wish item should be at least 3 characters"
    if len(postData['desc']) < 1:
      errors["desc"] = "Wish description must be provided"
    return errors 


class Wish(models.Model):
  item= models.CharField(max_length=255)
  desc = models.TextField()
  user = models.ForeignKey(User, related_name="wishes", on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = WishManager() 

class Granted(models.Model):
  status = models.BooleanField(default=False)
  wish = models.OneToOneField(Wish, related_name="granted", on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

class Like(models.Model):
  granted = models.ForeignKey(Granted, related_name="likes", on_delete = models.CASCADE)
  user = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
