from django.db import models
from django.core.validators import validate_email
import re
import bcrypt

class UserManager(models.Manager):
  def basic_validator(self, postData):
    errors = {}
    # agregue claves y valores al diccionario de errores para cada campo no válido
    if len(postData['first_name']) < 2:
      errors["first_name"] = "User first_name should be at least 2 characters"
    if len(postData['last_name']) < 2:
      errors["last_name"] = "User last_name should be at least 2 characters"
    if len(postData['password']) < 8:
      errors["password"] = "User password should be at least 8 characters"
    if len(postData['email']) < 1 :
      errors["email"] = "User email can`t be blank"
    user = self.filter(email=postData['email'])
    if user:
      errors["email"] = "ya existe el email"
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(postData['email']):    # probar si un campo coincide con el patrón        
      errors['email'] = "Invalid email address!"
    if postData['password'] != postData['confirm_password']:
      errors['password'] = "Passwords no coinciden"
    return errors

  def basic_validator2(self, postData):
    errors = {}
    if len(postData['email']) < 1:
      errors["email"] = "User email can't be blank"
    EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
    if not EMAIL_REGEX.match(postData['email']):    # probar si un campo coincide con el patrón        
      errors['email'] = "Invalid email address!"
    user = self.filter(email=postData['email'])
    if len(user) == 0:
      errors["email"] = " User email is incorrect"
    elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
      errors["password"] = "User password is incorrect"
    if len(postData['password']) < 1:
      errors["password"] = "User password can't be blank"

    return errors

class User(models.Model):
  first_name = models.CharField(max_length=50, blank=False, null=False)
  last_name = models.CharField(max_length=50, blank=False, null=False)
  email = models.EmailField(max_length=100, unique=True, blank=False, null=False)
  password = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  objects = UserManager() 
