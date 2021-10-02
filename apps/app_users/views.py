from django.shortcuts import render, redirect
from apps.app_users.models import User
import bcrypt
from django.contrib import messages

def index(request):
  try:
    context ={
      "user": User.objects.get(id= request.session['userid'])
    }
    return render(request, "app_users/index.html", context)
  except:
    context ={
      "user": None
    }
    return render(request, "app_users/index.html", context)

def register(request):
  errors = User.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:   
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()    
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], 
                        email= request.POST['email'], password=pw_hash)
    return redirect('/')

def login(request):
  errors = User.objects.basic_validator2(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/')
  else:  
    user = User.objects.filter(email=request.POST['email'])
    if user:
      logged_user = user[0]
      if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
        request.session['userid'] = logged_user.id
        return redirect('/wishes')
    return redirect('/')

def logout(request):
  if 'userid' in request.session:
    request.session.delete()
    print(request.session['userid'])  
    return redirect('/')
  else:
    messages.info(request, 'No puedes cerrar sesión si aun no has ingresado')
    return redirect('/')

