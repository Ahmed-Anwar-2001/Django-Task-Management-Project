from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import *
import json
from django.http import JsonResponse
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
@login_required(login_url='/login')  
def home(request):
    if request.user.is_authenticated:
        user = request.user
        tasks = Task.objects.filter(user=user)
    else:
        tasks = []  

    return render(request, 'home.html', {'tasks': tasks})

def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('pass1')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('/') 
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('/login')

def signup(request):
    if request.method=="POST":
        username = request.POST.get('username')
        first_name = request.POST.get('fname')
        last_name = request.POST.get('lname')
        password = request.POST.get('pass1')
        email = request.POST.get('email')
        print(username)

        if User.objects.filter(username=username).exists():
            messages.info(request, "User already exists.")
            return redirect("/signup")

        else:
            user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            email = email,
            username = username,

            )

            user.set_password(password)
            user.save()

            messages.success(request, 'Account created successfully.')
            return redirect("/login")

    return render(request, 'signup.html')
@login_required
def user_profile(request):
    user = request.user
    if request.method == 'POST':
        # Update user attributes directly
        user.username = request.POST.get('Username','')
        user.first_name = request.POST.get('First_name', '')
        user.last_name = request.POST.get('Last_name', '')
        user.email = request.POST.get('Email', '')
        print(user.username)
        user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'profile.html', {'user': user})

@staff_member_required
def user_list(request):
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

@staff_member_required
def view_user_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, 'view_user_profile.html', {'profile_user': user})

@staff_member_required
def make_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = MakeAdminForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User is now an admin!')
            return redirect('user_list')
    else:
        form = MakeAdminForm(instance=user)
    return render(request, 'make_admin.html', {'form': form, 'user': user})

@staff_member_required
def remove_admin(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.is_staff = False
        user.save()
        messages.success(request, 'Admin privileges removed successfully!')
        return redirect('user_list')
    return render(request, 'remove_admin.html', {'user': user})

@staff_member_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully!')
        return redirect('user_list')
    return render(request, 'delete_user.html', {'user': user})



def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        
        # Get the currently logged-in user
        user = request.user
        
        # Create the task
        task = Task.objects.create(
            user=user,
            title=title,
            description=description,
            due_date=due_date,
            priority=priority
        )
        
        return redirect('/')  
    return render(request, 'create_task.html')


def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    return redirect('/')

@login_required(login_url='/login')
def mark_as_complete(request):
    if request.method == 'POST':
        print('SSSS')
        data = json.loads(request.body)
        task_id = data.get('taskId')
        is_checked = data.get('isChecked')

        try:
            task = Task.objects.get(id=task_id)
            task.is_complete = is_checked
            task.save()
            return JsonResponse({'success': True})
        except Task.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Task not found'})
    
    return JsonResponse({'success': False, 'error': 'Invalid request'})

def task_detail(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'task_detail.html', {'task': task})


def add_photo(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST' and request.FILES.getlist('photo'):
        images = request.FILES.getlist('photo')
        for image in images:
            photo = Photo(task=task, image=image)
            photo.save()
        print(task.id)
        return redirect('task_detail', task_id=task.id)

    return render(request, 'add_photo.html', {'task': task})


def delete_selected_photos(request, task_id):
    if request.method == 'POST':
        selected_photos = request.POST.getlist('selected_photos')
        for photo_id in selected_photos:
            Photo.objects.filter(id=photo_id).delete()

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method'})



def update_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        priority = request.POST.get('priority')
        task.title = title
        task.description = description
        task.due_date = due_date
        task.priority = priority
        
        task.last_updated_at = timezone.now()
        
        task.save()
        return redirect('task_detail', task_id=task_id)
    return render(request, 'update_task.html', {'task': task})
