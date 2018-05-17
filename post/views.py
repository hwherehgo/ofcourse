from django.shortcuts import render,redirect
from .models import Post
from math import ceil
from .helpers import page_cache
from .helpers import read_count
from .helpers import get_top_n
# Create your views here.



@read_count
@page_cache(2)
def read(request):
    post_id = request.GET.get('post_id')
    data = Post.objects.get(id=post_id)
    return render(request,'read.html',{'data':data})

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title,content=content)
        return redirect('post/read/?post_id={}'.format(post.id))
    else:
        return render(request,'create.html')

def edit(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.content =request.POST.get('content')
        post.save()
        return redirect('post/read/?post_id=%s'%post_id)

    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(id = post_id)
        return render(request,'edit.html',{'post':post})


def search(request):
    if request.method == 'POST':
        keyword = request.POST.get('keyword')
        posts = Post.objects.filter(content__contains=keyword)
        return render(request,'search.html',{'posts':posts})


def post_list(request):
    page = request.GET.get('page')
    total = Post.objects.count()
    per_page = 5
    pages = ceil(total/per_page)

    start = (page-1)*per_page
    end = page*per_page
    posts = Post.objects.all().order_by('-id')[start:end]

    return render(request,'post_list.html',{'posts':posts,'pages':pages})

def rank_top(request):

    data = get_top_n(10)
    return render(request,'top10.html',{'data':data})