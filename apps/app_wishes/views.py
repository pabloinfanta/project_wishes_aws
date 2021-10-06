from django.shortcuts import render, redirect
from apps.app_users.models import User
from apps.app_wishes.models import Wish, Granted, Like
from django.contrib import messages

def index(request):
  if 'userid' in request.session: 
    user = User.objects.get(id = request.session['userid'])
    wishes= []
    for wish in user.wishes.all():
      if wish.granted.status == False:
        wishes.append(wish)

    wishes_granted = []
    for wish in Wish.objects.all():
      if wish.granted.status == True:
        wishes_granted.append(wish)

    context={
      "user": user,
      "wishes": wishes,
      "wishes_granted": wishes_granted
    }
    return render(request, "app_wishes/index.html", context)
  else:
    messages.info(request, "No puedes acceder a esta sección si no has iniciado sesión")
    return render(request, 'app_users/index.html')


def form_create(request):
  if 'userid' in request.session: 
    context={
      "user": User.objects.get(id = request.session['userid'])
    }
    return render(request, "app_wishes/form_create.html", context)
  else:
    messages.info(request, "No puedes acceder a esta sección si no has iniciado sesión")
    return render(request, 'app_users/index.html') 


def create_wish(request):
  errors = Wish.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect('/wishes/form_create')
  else:  
    user = User.objects.get(id= request.session['userid'])
    wish=Wish.objects.create(item = request.POST['item'], desc = request.POST['desc'], user = user)
    Granted.objects.create(status = False, wish= wish )
    return redirect('/wishes')

def delete_wish(request, id):
  wish = Wish.objects.get(id= id)
  wish.delete()
  return redirect('/wishes')

def form_edit(request, id):
  if 'userid' in request.session:
    context={
      "wish": Wish.objects.get(id=id),
      "user": User.objects.get(id = request.session['userid'])
    }
    return render(request, "app_wishes/form_edit.html", context)
  else:
    messages.info(request, "No puedes acceder a esta sección si no has iniciado sesión")
    return render(request, 'app_users/index.html')
    
def granted_wish(request, id):
  wish = Wish.objects.get(id= id)
  print(wish)
  granted= wish.granted
  granted.status = True
  granted.save()

  return redirect('/wishes') 

def update_wish(request, id):
  errors = Wish.objects.basic_validator(request.POST)
  if len(errors) > 0:
    for key, value in errors.items():
      messages.error(request, value)
    return redirect(f'/wishes/{id}/form_edit')
  else:  
    wish = Wish.objects.get(id= id)
    wish.item = request.POST['item']
    wish.desc = request.POST['desc']
    wish.save()
    return redirect('/wishes')

def stats(request):
  if 'userid' in request.session:
    user = User.objects.get(id = request.session['userid'])
    wishes_granted = []
    for wish in Wish.objects.all():
      if wish.granted.status == True:
        wishes_granted.append(wish)
    total_granted = len(wishes_granted)

    my_granted = []
    for wish in user.wishes.all():
      if wish.granted.status == True:
        my_granted.append(wish)
    total_my_granted = len(my_granted)

    pending_wishes= []
    for wish in user.wishes.all():
      if wish.granted.status == False:
        pending_wishes.append(wish)
    total_pending_wishes= len(pending_wishes)

    context={
      "user": user,
      "total_granted": total_granted,
      "total_my_granted": total_my_granted,
      "total_pending_wishes": total_pending_wishes
    }
    return render(request, "app_wishes/stats.html", context)
  else:
    messages.info(request, "No puedes acceder a esta sección si no has iniciado sesión")
    return render(request, 'app_users/index.html') 
  
def like(request, id):
  user = User.objects.get(id = request.session['userid'])
  granted = Wish.objects.get(id=id).granted
  if user == granted.wish.user:
    messages.info(request, "No puedes dar like a tu propio deseo")
    return redirect('/wishes')
  elif Like.objects.filter(user= user.id):
    messages.info(request, "No puedes dar mas de un like")
    return redirect('/wishes')
  else:  
    Like.objects.create(granted= granted, user= user)
    return redirect('/wishes')