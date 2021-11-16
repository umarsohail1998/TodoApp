from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest,HttpResponseRedirect, JsonResponse
from .models import Todo

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import json
# Create your views here.

def owner(request):
    if request.user.is_authenticated and request.user.is_superuser:
        data = list(Todo.objects.all().values('username', 'content', 'status')) 
        # print(data)
        
        dt = {}
        for x in data:
            try:
                if dt.__contains__(x["username"]):
                    dt[x["username"]].append({'status': x["status"], 'content': x["content"]}) 
                else:
                    dt[x["username"]] = []
                    dt[x["username"]].append({'status': x["status"], 'content': x["content"]}) 
            except Exception as e:
                print(e)
        print(dt)
        return JsonResponse(dt)
    return HttpResponse("Not have a permission")

def index(request):
    return HttpResponse("Index Page")

# Create your views here.
def list_todo_items(request):
    if request.user.is_authenticated:
        # return HttpResponseRedirect('/profile/')

        # data = Todo.objects.all()
        data = Todo.objects.filter(username=request.user)
        active = []
        completed = []
        for x in data:
            if x.status:
                completed.append(x)
            else:
                active.append(x)
        # print(active)
        # print(completed)
        context = {'active' :active , 'completed': completed, 'name': request.user}
        return render(request, 'todos/todo_list.html',context)
    return HttpResponseRedirect('/login/')

def insert_todo_item(request: HttpRequest):
    todo = Todo(content=request.POST['content'],username =request.user)
    todo.save()
    return redirect('/')

def delete_record(todo_id):
    todo_to_delete = Todo.objects.get(id=todo_id)
    todo_to_delete.delete()

def delete_todo_item(request,todo_id):
    tmp = request.POST['btn']
    if tmp == 'trash':
        delete_record(todo_id)
    elif request.POST['btn'] == 'complete':
        Todo.objects.filter(id=todo_id).update(status=True)
    
    # print(request.POST['btn'], todo_id)
    return redirect('/')

def sign_up(request):
    print("sign up")
    if request.user.is_authenticated:
        return HttpResponseRedirect('/profile/')

    if request.method == "POST":
        fm = SignUpForm(request.POST)
        if fm.is_valid():
            messages.success(request, "Account Created successfully !!")
            fm.save()
    else:
        fm = SignUpForm()
    return render(request, 'todos/signup.html', {'form': fm})

def user_login(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            fm = AuthenticationForm(request=request, data= request.POST)
            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user =  authenticate(username = uname, password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logges in Succesfully !!')
                    return HttpResponseRedirect('/profile/')
        else:
            fm =  AuthenticationForm()
        
        return render(request, 'todos/login.html', {'form': fm})
    return HttpResponseRedirect('/profile/')

def user_profile(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
        # return render(request, 'todos/profile.html', {'name': request.user})
    else:
        return HttpResponseRedirect('/login/')

def user_logout(request):
    # print("jello")
    # for x in range(100000):
    #     pass
    logout(request)
    return HttpResponseRedirect('/login/')
