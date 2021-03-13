from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .filters import PostFilter
from .forms import PostForm

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .models import *

# Create your views here.

def homepage(request):
    posts = Post.objects.filter(active=True, featured=True)[0:3]
    context={'posts':posts}
    return render (request, 'resume/index.html', context)

def postpage(request, slug):
    post = Post.objects.get(slug=slug)
    context={'post':post}
    return render (request, 'resume/post.html', context)

def posts(request):

    posts = Post.objects.filter(active=True)
    myfilter = PostFilter(request.GET, queryset=posts)
    posts = myfilter.qs

    context={'posts': posts, 'myfilter':myfilter}
    return render (request, 'resume/posts.html', context)

def profile(request):
    context={}
    return render (request, 'resume/profile.html', context)

@login_required(login_url="Home")
def createpost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('List')

    context={'form':form}
    return render (request, 'resume/post_form.html', context)

@login_required(login_url="Home")
def updatepost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('List')

    context={'form':form}
    return render (request, 'resume/post_form.html', context)

@login_required(login_url="Home")
def deletepost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('List')
    context={'item':post}
    return render (request, 'resume/delete.html', context)

def sendemail(request):
    
    if request.method == 'POST':
        template = render_to_string('resume/email_template.html', {
            'name':request.POST['name'],
            'email':request.POST['email'],
            'message':request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['codewar1python@gmail.com']
        )
        email.fail_silently = False
        email.send()
    return render(request,'resume/email_sent.html')