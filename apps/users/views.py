from django.shortcuts import render, redirect
from .models import User, Message, Comment, Description
from django.contrib import messages
import bcrypt

# Create your views here.


def index(request):

    return render(request, 'users/index.html')

def new(request):

    return render(request, 'users/register.html')


def create(request):
    postData = {
        'first_name' : request.POST['first_name'], 
        'last_name' : request.POST['last_name'], 
        'email' : request.POST['email'], 
        'pwd' : request.POST['pwd'], 
        'confirm_pwd' : request.POST['confirm_pwd']
    }

    user = User.objects.reg(postData)

    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/register')
    
    if 'theUser' in user:
        request.session['id'] = user['theUser'].id
        if user['theUser'].user_level == 9:
            request.session['admin'] = 1
            return redirect('/dashboard/admin')
        else:
            # if request.session['admin'] == 1:
            #     return redirect('/dashboard/admin')
            # else:
            return redirect('/dashboard')


    return redirect('/')

def login(request):

    return render(request, 'users/login.html')

def login_process(request):

    context = { 
        'email' : request.POST['email'], 
        'pwd' : request.POST['pwd'] 
    }
    user = User.objects.login(context)

    if 'error' in user:
        messages.warning(request, user['error'])
        return redirect('/')
    
    if 'theUser' in user:
        request.session['id'] = user['theUser'].id
        if user['theUser'].user_level == 9:
            request.session['admin'] = 1
            return redirect('/dashboard/admin')
        else:
            return redirect('/dashboard')


def dashboard_admin(request):

    context = {
        'users' : User.objects.all()
    }

    return render(request, 'users/dashboard_admin.html', context)

def add(request):

    return render(request, 'users/add.html')

def dashboard(request):

    context = {
        'users' : User.objects.all()
    }

    return render(request, 'users/dashboard.html', context)

def show(request, user_id):
    user = User.objects.get(id = user_id)
    active_user = User.objects.get(id = request.session['id'])
    messages = Message.objects.filter(to_user = User.objects.get(id = user_id)).order_by('-created_at')
    print active_user.user_level
    context = {
        'active_user' : active_user,
        'user' : user,
        'messages' : messages,
    }

    return render(request, 'users/show.html', context)

def message_process(request, user_id, active_user_id):

    Message.objects.create(content = request.POST['content'], to_user = User.objects.get(id = user_id), from_user = User.objects.get(id = active_user_id))

    address = '/users/show/' + str(user_id)
    return redirect(address)

def comment_process(request, message_id, user_id, active_user_id):

    Comment.objects.create(content = request.POST['content'], user = User.objects.get(id = active_user_id), message = Message.objects.get(id = message_id))

    address = '/users/show/' + str(user_id)
    return redirect(address)

def admin_edit(request, user_id):
    user = User.objects.get(id = user_id)
    print user
    context = {
        'user' : user
    }

    return render(request, 'users/admin_edit.html', context)

def update_info(request, user_id):
    user = User.objects.get(id = user_id)
    print user.first_name

    if request.POST['email']:
        user.email = request.POST['email']
    if request.POST['first_name']:
        user.first_name = request.POST['first_name']
    if request.POST['last_name']:
        user.last_name = request.POST['last_name']
    
    if request.POST['user_level']:
        if request.POST['user_level'] == 'admin':
            user.user_level = 9
        elif request.POST['user_level'] == 'normal':
            user.user_level = 1

    user.save()

    user = User.objects.get(id = request.session['id'])
    if user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def update_pwd(request, user_id):
    user = User.objects.get(id = user_id)

    if request.POST['pwd']:
        if request.POST['confirm_pwd'] != request.POST['pwd']:
            messages.warning(request, 'Not match password')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['pwd'].encode('utf-8'), bcrypt.gensalt())

            user.password = hashed_pw
    
    user.save()
    user = User.objects.get(id = request.session['id'])
    if user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')

def update_description(request, user_id):
    user = User.objects.get(id = user_id)

    if not Description.objects.filter(user = user):
        Description.objects.create(content = request.POST['description'], user = user)
    else:
        description = Description.objects.get(user = user)
        description.content = request.POST['description']
        description.save()

    user = User.objects.get(id = request.session['id'])
    if user.user_level == 9:
        return redirect('/dashboard/admin')
    else:
        return redirect('/dashboard')


def edit(request):
    active_user = User.objects.get(id = request.session['id'])
    context = {
        'active_user' : active_user
    }

    return render(request, 'users/edit.html', context)

def destroy(request, user_id):
    User.objects.get(id = user_id).delete()

    return redirect('/dashboard/admin')



def logoff(request):
    request.session.clear()
    return redirect('/')